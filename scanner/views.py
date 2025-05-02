from django.http import StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files import File
from django.conf import settings
from .models import ScanRecord, CustomUser
from .serializers import ContactSerializer, RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
import os, shutil, threading, subprocess
from time import sleep

class ScanView(APIView):
    def post(self, request):
        ip = request.data.get("ip")
        scan_type = request.data.get("scanType")

        if not ip:
            return Response({"error": "IP address is required"}, status=400)

        scan_record = ScanRecord.objects.create(ip=ip, scan_type=scan_type)

        def run_scan():
            scan_args = {
                'tcp': ['nmap', '-sT', '-T4', '-sV', '-O', '-p', '1-65535', '-vv', ip],
                'udp': ['nmap', '-sU', '-T4', '-sV', '-O', '-p', '1-65535', '-vv', ip],
                'full': ['nmap', '-sS', '-sU', '-T4', '-sV', '-O', '-p-', '-vv', ip]
            }.get(scan_type, ['nmap', '-sT', '-vv', ip])

            xml_dir = os.path.join(settings.MEDIA_ROOT, 'scans', 'xml')
            html_dir = os.path.join(settings.MEDIA_ROOT, 'scans', 'html')
            os.makedirs(xml_dir, exist_ok=True)
            os.makedirs(html_dir, exist_ok=True)

            xml_path = os.path.join(xml_dir, f"scan_{scan_record.id}.xml")
            html_path = os.path.join(html_dir, f"scan_{scan_record.id}.html")

            scan_args += ['-oX', xml_path]
            process = subprocess.Popen(scan_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

            output_lines = []
            for line in process.stdout:
                output_lines.append(line)
                scan_record.output = ''.join(output_lines)
                scan_record.save()

            xsltproc_path = shutil.which("xsltproc")
            if xsltproc_path:
                subprocess.run([xsltproc_path, xml_path, '-o', html_path])
            else:
                print("xsltproc not found")

            with open(xml_path, 'rb') as f:
                scan_record.xml_file.save(f"scan_{scan_record.id}.xml", File(f), save=False)
            with open(html_path, 'rb') as f:
                scan_record.html_file.save(f"scan_{scan_record.id}.html", File(f), save=False)

            scan_record.completed = True
            scan_record.save()

        threading.Thread(target=run_scan).start()
        return Response({"scan_id": scan_record.id}, status=201)

class ScanResultView(APIView):
    def get(self, request, scan_id):
        try:
            scan_record = ScanRecord.objects.get(id=scan_id)
        except ScanRecord.DoesNotExist:
            return Response({"error": "Scan not found"}, status=404)

        # Common response data
        response_data = {
            "scan_id": scan_record.id,
            "ip": scan_record.ip,
            "scan_type": scan_record.scan_type,
            "status": "completed" if scan_record.completed else "in_progress"
        }

        # Check if this is an SSE request by examining headers
        is_sse = 'text/event-stream' in request.META.get('HTTP_ACCEPT', '')

        if is_sse:
            if scan_record.completed:
                return Response(
                    {"error": "Scan already completed"},
                    status=400,
                    content_type='application/json'
                )
                
            def event_stream():
                last_output = ""
                while True:
                    try:
                        scan_record.refresh_from_db()
                        if scan_record.output != last_output:
                            yield f"data: {scan_record.output[len(last_output):]}\n\n"
                            last_output = scan_record.output
                        if scan_record.completed:
                            yield "event: complete\ndata: {\"status\": \"completed\"}\n\n"
                            break
                        sleep(1)
                    except Exception as e:
                        yield f"event: error\ndata: {str(e)}\n\n"
                        break

            response = StreamingHttpResponse(
                event_stream(),
                content_type='text/event-stream'
            )
            response['Cache-Control'] = 'no-cache'
            return response

        # For regular requests
        if scan_record.completed:
            response_data.update({
                "output": scan_record.output,
                "xml_file": scan_record.xml_file.url if scan_record.xml_file else None,
                "html_file": scan_record.html_file.url if scan_record.html_file else None
            })
        
        return Response(response_data)


class ContactFormView(APIView):
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Message sent successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=201)
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful',
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=200)
        elif CustomUser.objects.filter(email=email).exists():
            return Response({'error': 'Incorrect password'}, status=401)
        else:
            return Response({'error': 'User not found. Please sign up.'}, status=404)

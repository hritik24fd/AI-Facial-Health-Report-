
    
let stream = null;
    let capturedImageData = null;
    let analysisResults = null;

    function showPage(pageId) {
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
        });
        document.getElementById(pageId).classList.add('active');
    }

    function showLoading(show) {
        document.getElementById('loadingOverlay').classList.toggle('active', show);
    }

    function goToDashboard() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            stream = null;
        }
        showPage('dashboard');
    }

    function startScanner() {
        showPage('camera');
        navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } })
            .then(s => {
                stream = s;
                document.getElementById('video').srcObject = stream;
            })
            .catch(err => {
                alert('Unable to access camera. Please grant camera permissions.');
                console.error(err);
            });
    }

    function capturePhoto() {
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        ctx.drawImage(video, 0, 0);

        capturedImageData = canvas.toDataURL('image/jpeg');
        document.getElementById('photoPreview').src = capturedImageData;

        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            stream = null;
        }

        showPage('review');
    }

    function retakePhoto() {
        showPage('camera');
        navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } })
            .then(s => {
                stream = s;
                document.getElementById('video').srcObject = stream;
            });
    }

    function analyzePhoto() {
        showLoading(true);

        const canvas = document.getElementById('canvas');
        canvas.toBlob(function (blob) {
            const formData = new FormData();
            formData.append("file", blob, "photo.jpg");

            fetch("http://localhost:8000/analyze", {
                method: "POST",
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                showLoading(false);
                displayResults(data);
            })
            .catch(err => {
                showLoading(false);
                alert('Error analyzing photo. Please try again.');
                console.error(err);
            });
        }, 'image/jpeg');
    }

    function displayResults(data) {
        analysisResults = data;
        
        document.getElementById('ageResult').textContent = data[0] || '-';
        document.getElementById('genderResult').textContent = data[1] || '-';
        document.getElementById('stressResult').textContent = data[2] || '-';
        document.getElementById('bpResult').textContent = data[3] || '-';
        document.getElementById('bsResult').textContent = data[4] || '-';
        
        document.getElementById('resultPhoto').src = capturedImageData;
        
        showPage('results');
    }

   function downloadPDF() {
    const pdfWindow = window.open('', '_blank');
    const currentDate = new Date().toLocaleDateString();
    const currentTime = new Date().toLocaleTimeString();

    const pdfContent = `
<!DOCTYPE html>
<html>
<head>
<title>Health Report</title>
<style>
body { font-family: Arial, sans-serif; padding: 40px; max-width: 800px; margin: 0 auto; }
h1 { color: #2c3e50; text-align: center; margin-bottom: 30px; }
.photo { width: 200px; height: 200px; margin: 20px auto; display: block; border-radius: 8px; border: 2px solid #dee2e6; }
.results { margin-top: 30px; border: 1px solid #dee2e6; border-radius: 8px; overflow: hidden; }
.result-row { padding: 20px; border-bottom: 1px solid #dee2e6; display: flex; justify-content: space-between; background: white; }
.result-row:last-child { border-bottom: none; }
.result-row:nth-child(even) { background: #f8f9fa; }
.label { font-weight: 600; color: #495057; }
.value { color: #2c3e50; font-weight: 600; }
.footer { margin-top: 40px; text-align: center; color: #6c757d; font-size: 12px; padding: 20px; background: #f8f9fa; border-radius: 8px; }
</style>
</head>
<body>

<h1>🏥 Health Face Scanner Report</h1>
<img src="${capturedImageData}" class="photo" />

<div class="results">
    <div class="result-row"><span class="label">Age Range:</span><span class="value">${analysisResults[0]}</span></div>
    <div class="result-row"><span class="label">Gender:</span><span class="value">${analysisResults[1]}</span></div>
    <div class="result-row"><span class="label">Stress Level:</span><span class="value">${analysisResults[2]}</span></div>
    <div class="result-row"><span class="label">Blood Pressure:</span><span class="value">${analysisResults[3]}</span></div>
    <div class="result-row"><span class="label">Blood Sugar:</span><span class="value">${analysisResults[4]}</span></div>
</div>

<div class="footer">
<strong>Generated on ${currentDate} at ${currentTime}</strong><br>
This report is for informational purposes only and should not replace professional medical advice.
</div>

<\/body>
<\/html>
`;

    pdfWindow.document.write(pdfContent);
    pdfWindow.document.close();

    setTimeout(() => {
        pdfWindow.print();
    }, 500);
}

    function startOver() {
        capturedImageData = null;
        analysisResults = null;
        showPage('dashboard');
    }

const canvas = document.getElementById('signature-pad');
const ctx = canvas.getContext('2d');
let drawing = false;

canvas.addEventListener('mousedown', () => drawing = true);
canvas.addEventListener('mouseup', () => drawing = false);
canvas.addEventListener('mouseout', () => drawing = false);
canvas.addEventListener('mousemove', draw);

canvas.addEventListener('touchstart', e => {
    e.preventDefault();
    drawing = true;
});
canvas.addEventListener('touchend', e => {
    e.preventDefault();
    drawing = false;
});
canvas.addEventListener('touchmove', e => {
    e.preventDefault();
    let touch = e.touches[0];
    let rect = canvas.getBoundingClientRect();
    let mouseEvent = new MouseEvent("mousemove", {
        clientX: touch.clientX - rect.left,
        clientY: touch.clientY - rect.top
    });
    canvas.dispatchEvent(mouseEvent);
});

function draw(e) {
    if (!drawing) return;
    const rect = canvas.getBoundingClientRect();
    const x = (e.clientX || e.touches?.[0]?.clientX) - rect.left;
    const y = (e.clientY || e.touches?.[0]?.clientY) - rect.top;

    ctx.lineWidth = 2;
    ctx.lineCap = 'round';
    ctx.strokeStyle = '#000';

    ctx.lineTo(x, y);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x, y);
}

function clearPad() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.beginPath();
}

// قبل ارسال فرم، داده‌ی امضا رو ذخیره کن
document.querySelector('form').addEventListener('submit', function () {
    const dataURL = canvas.toDataURL();
    document.getElementById('signature-data').value = dataURL;
});
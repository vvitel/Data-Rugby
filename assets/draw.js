window.trigger = () => {
  const canvas = document.querySelector("#canvas");
  const ctx = canvas.getContext("2d");
  const pos = { x: 0, y: 0 };
  let isDrawing = false;

  function setPosition(e) {
    const rect = canvas.getBoundingClientRect();
    pos.x = e.clientX - rect.left;
    pos.y = e.clientY - rect.top;
  }

  function resize() {
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width;
    canvas.height = rect.height;
  }

  function startDrawing(e) {
    isDrawing = true;
    setPosition(e);
  }

  function stopDrawing() {
    isDrawing = false;
  }

  function draw(e) {
    if (!isDrawing) {
      setPosition(e);
      return;
    }

    ctx.beginPath();
    ctx.lineWidth = 5;
    ctx.lineCap = "round";
    ctx.strokeStyle = "#f1de0cff";

    ctx.moveTo(pos.x, pos.y);
    setPosition(e);
    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
  }

  window.addEventListener("resize", resize);
  canvas.addEventListener("mousedown", startDrawing);
  canvas.addEventListener("mouseup", stopDrawing);
  canvas.addEventListener("mouseout", stopDrawing);
  canvas.addEventListener("mousemove", draw);

  resize(); // Redimensionne une première fois après chargement
};

// Exécuter le code après le chargement complet de la page
window.onload = () => {
  window.trigger();
};


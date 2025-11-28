document.addEventListener("DOMContentLoaded", () => {
  const sidebar = document.getElementById("sidebar");
  const toggleBtn = document.getElementById("toggle-btn");
  const isMobile = window.matchMedia("(max-width:37em)").matches;

  if(isMobile){
    sidebar.classList.add("collapsed");
  }

  toggleBtn.addEventListener("click", () => {
    sidebar.classList.toggle("collapsed");
  });
});

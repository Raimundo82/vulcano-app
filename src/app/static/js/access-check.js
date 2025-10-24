/**
 * Função genérica para verificar acesso a uma rota via AJAX.
 * Pode ser reutilizada por qualquer página protegida.
 */

 function showAccessPopup(message) {
      Swal.fire({
        icon: "error",
        title: "Acesso Restrito",
        text: message,
        confirmButtonText: "OK",
        backdrop: true,
      });
}

function setupAccessCheck(route, defaultErrorMessage) {
  document.addEventListener("DOMContentLoaded", function () {
    fetch(route, {
      headers: { "X-Requested-With": "XMLHttpRequest" },
    })
      .then((response) => {
        if (response.status === 403) {
          return response.json().then((data) => {
            showAccessPopup(data.message);
          });
        }
        return response.text();
      })
      .catch(() => {
        showAccessPopup(defaultErrorMessage);
      });
  });
}
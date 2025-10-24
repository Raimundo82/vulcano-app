$(document).ready(function () {
  const table = $("#faturasTable").DataTable({
    ajax: { url: apiEndpoint, dataSrc: "" },
    columns: [
      { data: "invoice_type" },
      {
        data: "invoice_number",
        render: (data, type, row) =>
          `<a href="/processed/${row.invoice_period_year}/${row.invoice_period_month}/${row.pdffile}" target="_blank">${data}</a>`,
      },
      { data: "issue_date" },
      { data: "taxpayer_number" },
      { data: "account_number" },
      { data: "client" },
      { data: "invoice_period_year" },
      { data: "invoice_period_month" },
      { data: "amount_to_pay" },
      { data: "total_amount" },
    ],
  });

  // Atualiza total mensal
  function updateTotalMensal() {
    let total = 0;
    table.rows({ search: "applied" }).data().each((r) => {
      if (r.total_amount) total += Number.parseFloat(r.total_amount);
    });
    $("#totalMensal").text(total.toFixed(2) + " €");
  }

  table.on("draw", updateTotalMensal);

  // filtros
  $("#ano, #mes").on("change", function () {
    table.column(6).search($("#ano").val()).column(7).search($("#mes").val()).draw();
  });

  // carrega anos/meses
  $.get(apiEndpoint, function (data) {
    const anos = [...new Set(data.map((d) => d.invoice_period_year))];
    const meses = [...new Set(data.map((d) => d.invoice_period_month))];
    for (const a of anos) {
      $("#ano").append(`<option value="${a}">${a}</option>`);
    }
    for (const m of meses) {
      $("#mes").append(`<option value="${m}">${m}</option>`);
    }
  });
});
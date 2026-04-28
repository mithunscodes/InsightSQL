const PALETTE = [
  "#6c63ff","#f59e0b","#10b981","#ef4444",
  "#3b82f6","#ec4899","#8b5cf6","#14b8a6",
];

async function fetchJSON(url) {
  const res = await fetch(url);
  return res.json();
}

async function initDashboard() {
  const [monthly, categories] = await Promise.all([
    fetchJSON("/api/monthly-revenue"),
    fetchJSON("/api/category-revenue"),
  ]);

  // Monthly Revenue Line Chart
  const revenueCtx = document.getElementById("revenueChart");
  if (revenueCtx) {
    new Chart(revenueCtx, {
      type: "line",
      data: {
        labels: monthly.map(r => {
          const d = new Date(r.year, r.month - 1);
          return d.toLocaleString("default", { month: "short", year: "2-digit" });
        }),
        datasets: [{
          label: "Revenue ($)",
          data: monthly.map(r => Number(r.revenue)),
          borderColor: "#6c63ff",
          backgroundColor: "rgba(108,99,255,0.12)",
          fill: true,
          tension: 0.4,
          pointRadius: 5,
          pointBackgroundColor: "#6c63ff",
        }],
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: ctx => ` $${ctx.parsed.y.toLocaleString("en-US", { minimumFractionDigits: 2 })}`,
            },
          },
        },
        scales: {
          x: { grid: { color: "rgba(255,255,255,0.04)" }, ticks: { color: "#8892a4" } },
          y: {
            grid: { color: "rgba(255,255,255,0.04)" },
            ticks: {
              color: "#8892a4",
              callback: v => `$${(v / 1000).toFixed(1)}k`,
            },
          },
        },
      },
    });
  }

  // Category Doughnut Chart
  const catCtx = document.getElementById("categoryChart");
  if (catCtx) {
    new Chart(catCtx, {
      type: "doughnut",
      data: {
        labels: categories.map(r => r.category),
        datasets: [{
          data: categories.map(r => Number(r.revenue)),
          backgroundColor: PALETTE,
          borderWidth: 2,
          borderColor: "#1a1d27",
        }],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: "bottom",
            labels: { color: "#e2e8f0", padding: 16, font: { size: 12 } },
          },
          tooltip: {
            callbacks: {
              label: ctx => ` $${Number(ctx.parsed).toLocaleString("en-US", { minimumFractionDigits: 2 })}`,
            },
          },
        },
      },
    });
  }
}

document.addEventListener("DOMContentLoaded", initDashboard);

import MonthlyReport from "./monthlyreport";
import ClosingStockReport from "./closingstockreport";

function ReportsDashboard() {
  return (
    <div style={{ padding: "20px" }}>
      <h1>Reports Dashboard</h1>

      <MonthlyReport />
      <hr />
      <ClosingStockReport />
    </div>
  );
}

export default ReportsDashboard;

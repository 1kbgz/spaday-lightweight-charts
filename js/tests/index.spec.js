import { expect, test } from "@playwright/test";

test("renders and reactively updates a chart", async ({ page }) => {
  await page.goto("/dist/index.html");
  await page.evaluate(() => {
    const chart = document.createElement("lightweight-chart");
    chart.style.width = "640px";
    chart.style.height = "300px";
    chart.type = "area";
    chart.theme = "dark";
    chart.data = [
      { time: "2026-01-01", value: 10 },
      { time: "2026-01-02", value: 12 },
    ];
    document.body.appendChild(chart);
  });

  await expect(page.locator("lightweight-chart canvas").first()).toBeVisible();
  await expect(page.locator("lightweight-chart")).toHaveJSProperty(
    "theme",
    "dark",
  );
  await page.locator("lightweight-chart").evaluate((chart) => {
    chart.data = [{ time: "2026-01-03", value: 15 }];
  });
  await expect(page.locator("lightweight-chart")).toHaveJSProperty("data", [
    { time: "2026-01-03", value: 15 },
  ]);
});

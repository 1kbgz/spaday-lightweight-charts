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

test("runs the Python dashboard with live server prices", async ({ page }) => {
  await page.goto("http://127.0.0.1:8011");
  const chart = page.locator("lightweight-chart").first();
  await expect(chart.locator("canvas").first()).toBeVisible();
  const initial = await chart.evaluate((element) => element.data.at(-1).value);
  await expect
    .poll(() => chart.evaluate((element) => element.data.at(-1).value), {
      timeout: 5_000,
    })
    .not.toBe(initial);
  await page.getByRole("button", { name: "Line" }).click();
  await expect(chart).toHaveJSProperty("type", "line");
});

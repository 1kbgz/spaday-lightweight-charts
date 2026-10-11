import fs from "node:fs";
import { expect, test } from "@playwright/test";

const errorsByPage = new WeakMap();

test.beforeEach(async ({ page }) => {
  test.skip(
    !fs.existsSync("dist/lite/index.html"),
    "run make test-pyodide-example first",
  );
  test.setTimeout(240_000);
  const errors = [];
  errorsByPage.set(page, errors);
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto("/dist/lite/");
  await page.waitForFunction(
    () =>
      document.documentElement.dataset.ready === "true" ||
      document.querySelector("#pyodide-status")?.textContent ===
        "Unable to start",
    undefined,
    { timeout: 180_000 },
  );
  await expect(page.locator("#pyodide-error")).toBeHidden();
  await expect(page.locator("html")).toHaveAttribute("data-ready", "true");
});

test.afterEach(async ({ page }) => {
  if (errorsByPage.has(page)) expect(errorsByPage.get(page)).toEqual([]);
});

test("renders Python charts with a live transports feed and working controls", async ({
  page,
}) => {
  await expect(
    page.getByRole("heading", { name: "Lightweight Charts dashboard" }),
  ).toBeVisible();
  const charts = page.locator("lightweight-chart");
  await expect(charts).toHaveCount(3);
  for (const chart of await charts.all()) {
    await expect(chart.locator("canvas").first()).toBeVisible();
    expect(await chart.evaluate((node) => node.data.length)).toBe(60);
  }
  const price = charts.first();
  const initial = await price.evaluate((node) => JSON.stringify(node.data));
  const metric = await page.locator(".metrics strong").first().textContent();
  await expect
    .poll(() => price.evaluate((node) => JSON.stringify(node.data)))
    .not.toBe(initial);
  await expect(page.locator(".metrics strong").first()).not.toHaveText(metric);
  await page.getByRole("button", { name: "Line", exact: true }).click();
  await expect.poll(() => price.evaluate((node) => node.type)).toBe("line");
  await page.getByRole("button", { name: "Histogram", exact: true }).click();
  await expect
    .poll(() => price.evaluate((node) => node.type))
    .toBe("histogram");
  await page.getByRole("button", { name: "Toggle theme" }).click();
  await expect(page.locator(".dashboard")).toHaveClass(/dark/);
  expect(
    await charts.evaluateAll((nodes) => nodes.map((node) => node.theme)),
  ).toEqual(["dark", "dark", "dark"]);
  await expect(page.locator("#pyodide-error")).toBeHidden();
});

test("keeps canvases mounted and scroll stable across Python updates", async ({
  page,
}) => {
  await page.setViewportSize({ width: 800, height: 400 });
  const charts = page.locator("lightweight-chart");
  await charts.evaluateAll((nodes) => {
    globalThis.initialCanvases = nodes.map((node) =>
      node.querySelector("canvas"),
    );
  });
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  const scroll = await page.evaluate(() => window.scrollY);
  expect(scroll).toBeGreaterThan(0);
  const initial = await charts
    .first()
    .evaluate((node) => JSON.stringify(node.data));
  await expect
    .poll(() => charts.first().evaluate((node) => JSON.stringify(node.data)))
    .not.toBe(initial);
  expect(
    await charts.evaluateAll((nodes) =>
      nodes.every(
        (node, i) =>
          node.querySelector("canvas") === globalThis.initialCanvases[i],
      ),
    ),
  ).toBe(true);
  expect(await page.evaluate(() => window.scrollY)).toBeCloseTo(scroll, 0);
});

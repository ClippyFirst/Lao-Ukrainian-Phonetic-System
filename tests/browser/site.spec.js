import { test, expect } from "@playwright/test";

test("Lao input produces visible Ukrainian and IPA results", async ({ page }) => {
  await page.goto("/");
  await page.locator("#lao-input").fill("ຂາ");
  await expect(page.locator("#results")).toBeVisible();
  await expect(page.locator("#output")).toHaveText("к'а");
  await expect(page.locator("#ipa")).toHaveText("kʰaː");
  await expect(page.locator("#analysis-status")).toContainText("ГОТОВО");
});

test("mixed-script input fails closed instead of fabricating output", async ({ page }) => {
  await page.goto("/");
  await page.locator("#lao-input").fill("ກа");
  await expect(page.locator("#results")).toBeVisible();
  await expect(page.locator("#analysis-status")).toContainText("НЕ ВСТАНОВЛЕНО");
  await expect(page.locator("#output")).toContainText("не пройшов перевірку");
});

test("clear control restores the empty state", async ({ page }) => {
  await page.goto("/");
  await page.locator("#lao-input").fill("ຂາ");
  await expect(page.locator("#output")).toHaveText("к'а");
  await page.locator("#clear").click();
  await expect(page.locator("#results")).toBeHidden();
  await expect(page.locator("#empty-state")).toBeVisible();
});

test("romanization mode is explicitly separate from IPA-first mode", async ({ page }) => {
  await page.goto("/");
  await page.locator("#lao-input").fill("ຂາ");
  await page.locator("#mode-romanization").click();
  await expect(page.locator("#mode-romanization")).toHaveAttribute("aria-pressed", "true");
  await expect(page.locator("#romanization-trace")).toBeVisible();
  await page.locator("#mode-phonetic").click();
  await expect(page.locator("#mode-phonetic")).toHaveAttribute("aria-pressed", "true");
  await expect(page.locator("#output")).toHaveText("к'а");
});

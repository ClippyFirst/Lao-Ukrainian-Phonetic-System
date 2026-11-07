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


test("keyboard users can reach the main tool through the skip link", async ({ page }) => {
  await page.goto("/");
  await page.keyboard.press("Tab");
  const skipLink = page.getByRole("link", { name: "Перейти до інструмента" });
  await expect(skipLink).toBeFocused();
  await expect(skipLink).toBeVisible();
  await page.keyboard.press("Enter");
  await expect(page.locator("#lao-input")).toBeFocused();
  await page.keyboard.type("ຂາ");
  await expect(page.locator("#output")).toHaveText("к'а");
  for (const selector of ["#example", "#example-complex", "#clear", "#copy", "#mode-phonetic", "#mode-romanization"]) {
    await page.keyboard.press("Tab");
    await expect(page.locator(selector)).toBeFocused();
  }
  await page.keyboard.press("Enter");
  await expect(page.locator("#mode-romanization")).toHaveAttribute("aria-pressed", "true");
});

test("the service exposes named landmarks, controls, and live result announcements", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("banner")).toBeVisible();
  await expect(page.getByRole("navigation", { name: "Основна навігація" })).toBeVisible();
  await expect(page.getByRole("main")).toBeVisible();
  await expect(page.getByRole("textbox", { name: "Лаоський текст" })).toBeVisible();
  await expect(page.getByRole("group", { name: "Швидкі приклади" })).toBeVisible();
  await page.locator("#lao-input").fill("ຂາ");
  await expect(page.getByRole("group", { name: "Метод українського запису" })).toBeVisible();
  await expect(page.locator("#output")).toHaveAttribute("aria-live", "polite");
  await expect(page.locator("#status")).toHaveAttribute("role", "status");
  await expect(page.locator(".trace-summary")).toHaveCount(2);
});

test("mobile and tablet reflow layouts do not overflow horizontally", async ({ page }) => {
  for (const width of [320, 390, 640, 768]) {
    await page.setViewportSize({ width, height: 900 });
    await page.goto("/");
    await page.locator("#lao-input").fill("ຂາ");
    await expect(page.locator("#output")).toHaveText("к'а");
    const layout = await page.evaluate(() => ({
      viewport: window.innerWidth,
      document: document.documentElement.scrollWidth,
      body: document.body.scrollWidth,
      output: document.querySelector("#output").getBoundingClientRect().right
    }));
    expect(layout.document, `document overflows at ${width}px`).toBeLessThanOrEqual(layout.viewport);
    expect(layout.body, `body overflows at ${width}px`).toBeLessThanOrEqual(layout.viewport);
    expect(layout.output, `output exceeds viewport at ${width}px`).toBeLessThanOrEqual(layout.viewport);
  }
});

test("200-percent text zoom keeps the input and result usable without horizontal overflow", async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 900 });
  await page.goto("/");
  await page.locator("#lao-input").fill("ຂາ");
  await page.addStyleTag({ content: "html { zoom: 2; }" });
  await expect(page.locator("#output")).toHaveText("к'а");
  const layout = await page.evaluate(() => ({
    viewport: document.documentElement.clientWidth,
    document: document.documentElement.scrollWidth,
    input: document.querySelector("#lao-input").getBoundingClientRect(),
    output: document.querySelector("#output").getBoundingClientRect()
  }));
  expect(layout.document).toBeLessThanOrEqual(layout.viewport);
  expect(layout.input.width).toBeGreaterThan(0);
  expect(layout.output.width).toBeGreaterThan(0);
  expect(layout.input.right).toBeLessThanOrEqual(layout.viewport);
  expect(layout.output.right).toBeLessThanOrEqual(layout.viewport);
});



test("touch emulation can use quick examples and switch output methods", async ({ browser }) => {
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    isMobile: true,
    hasTouch: true
  });
  const page = await context.newPage();
  await page.goto("/");
  await page.locator("#example").tap();
  await expect(page.locator("#output")).toHaveText("к'а");
  await page.locator("#mode-romanization").tap();
  await expect(page.locator("#mode-romanization")).toHaveAttribute("aria-pressed", "true");
  await context.close();
});


test("browser UI labels grapheme fallback as provisional and keeps accepted output withheld", async ({ page }) => {
  await page.goto("/");
  await page.locator("#lao-input").fill("ກາລ");
  await expect(page.locator(".grapheme-preview")).toContainText("PROVISIONAL");
  await expect(page.locator(".grapheme-preview")).toContainText("kaː");
  await expect(page.locator("#output")).not.toContainText("к'а");
  await expect(page.locator(".grapheme-preview")).toContainText("ລ");
});


test("every interactive control has a programmatic accessible name", async ({ page }) => {
  await page.goto("/");
  const unnamed = await page.locator("button, a, textarea, summary").evaluateAll((elements) =>
    elements.filter((element) => {
      const labelledBy = element.getAttribute("aria-labelledby");
      const labelledByText = labelledBy
        ? labelledBy.split(/\s+/).map((id) => document.getElementById(id)?.textContent || "").join(" ").trim()
        : "";
      const label = element.labels ? Array.from(element.labels).map((node) => node.textContent || "").join(" ").trim() : "";
      const name = element.getAttribute("aria-label") || labelledByText || label ||
        element.getAttribute("title") || element.textContent?.trim() || "";
      return !name;
    }).map((element) => element.outerHTML)
  );
  expect(unnamed, "interactive elements without accessible names").toEqual([]);
});

test("methodology page exposes keyboard-accessible navigation and a named main landmark", async ({ page }) => {
  await page.goto("/system.html");
  await expect(page.getByRole("banner")).toBeVisible();
  await expect(page.getByRole("navigation", { name: "Основна навігація" })).toBeVisible();
  await expect(page.getByRole("navigation", { name: "Навігація методологією" })).toBeVisible();
  await expect(page.getByRole("main")).toBeVisible();
  await expect(page.getByRole("heading", { level: 1 })).toHaveCount(1);
  await page.keyboard.press("Tab");
  await expect(page.getByRole("link", { name: "Перейти до методології" })).toBeFocused();
  await page.keyboard.press("Enter");
  await expect(page).toHaveURL(/#main$/);
});

test("forced-colors and reduced-motion preferences retain visible focus and suppress motion", async ({ page }) => {
  await page.goto("/");
  await page.emulateMedia({ forcedColors: "active" });
  await page.keyboard.press("Tab");
  const forced = await page.locator(".skip-link").evaluate((element) => ({
    active: matchMedia("(forced-colors: active)").matches,
    outlineStyle: getComputedStyle(element).outlineStyle
  }));
  expect(forced.active).toBe(true);
  expect(forced.outlineStyle).not.toBe("none");
  await page.emulateMedia({ reducedMotion: "reduce" });
  const reduced = await page.locator("html").evaluate((element) => ({
    active: matchMedia("(prefers-reduced-motion: reduce)").matches,
    scrollBehavior: getComputedStyle(element).scrollBehavior
  }));
  expect(reduced.active).toBe(true);
  expect(reduced.scrollBehavior).toBe("auto");
});

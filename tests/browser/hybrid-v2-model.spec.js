import { test, expect } from "@playwright/test";

test.skip(
  process.env.HYBRID_V2_MODEL_AVAILABLE !== "1",
  "Full local model assets are assembled only in the GitHub Pages deployment build.",
);

test("Hybrid v2 runs beam-five tonal inference locally from Pages assets", async ({ page }) => {
  test.setTimeout(120000);
  const externalRequests = [];
  const pageErrors = [];
  page.on("request", (request) => {
    const url = request.url();
    if (url.startsWith("http://") && !url.startsWith("http://127.0.0.1:4173")) {
      externalRequests.push(url);
    }
    if (url.startsWith("https://")) externalRequests.push(url);
  });
  page.on("pageerror", (error) => pageErrors.push(error.message));

  await page.goto("/");
  const input = page.locator("#lao-input");
  const run = page.locator("#run-hybrid-v2");
  const status = page.locator("#hybrid-v2-status");
  const ipa = page.locator("#hybrid-v2-ipa");
  const alignment = page.locator("#hybrid-v2-alignment");
  const meta = page.locator("#hybrid-v2-meta");

  await input.fill("ຂາ");
  await expect(run).toBeEnabled();
  const coldStart = Date.now();
  await run.click();
  await expect.poll(
    async () => status.textContent(),
    { timeout: 60000, intervals: [250, 500, 1000] },
  ).toMatch(/Hybrid v2 завершив аналіз|Нейромережевий канал не запустився/);
  const coldStatus = await status.textContent();
  expect(coldStatus).toContain("Hybrid v2 завершив аналіз");
  const coldStartMs = Date.now() - coldStart;

  await expect(ipa).not.toBeEmpty();
  await expect(alignment).toContainText("ORDER_ALIGNED");
  await expect(meta).toContainText("beam=5");
  await expect(meta).toContainText("e02608cfcb18abfe6b1916f5f4774bfac9ac788d");

  await page.evaluate(() => {
    window.__hybridV2StatusChanges = [];
    const target = document.querySelector("#hybrid-v2-status");
    new MutationObserver(() => {
      window.__hybridV2StatusChanges.push(target.textContent);
    }).observe(target, { childList: true, characterData: true, subtree: true });
  });
  const warmStart = Date.now();
  await run.click();
  // Observe the loading transition as well as completion. This remains reliable
  // when cached WASM inference is faster than Playwright's next assertion.
  await expect.poll(
    () => page.evaluate(() => window.__hybridV2StatusChanges),
    { timeout: 10000, intervals: [50, 100, 250] },
  ).toContain("Підготовка локальної нейромережі…");
  await expect.poll(
    async () => status.textContent(),
    { timeout: 30000, intervals: [50, 100, 250] },
  ).toContain("Hybrid v2 завершив аналіз");
  const warmStartMs = Date.now() - warmStart;

  // Multi-syllable IPA remains visible even when the external parser cannot
  // uniquely associate tone contours; the UI must not invent associations.
  await input.fill("ສະບາຍດີ");
  await expect(run).toBeEnabled();
  await run.click();
  await expect.poll(
    async () => status.textContent(),
    { timeout: 30000, intervals: [50, 100, 250] },
  ).toContain("Сирий нейромережевий IPA збережено");
  await expect(ipa).toContainText("sa˧˥baːɲiː˧˥diː");
  await expect(alignment).toContainText("NOT_ALIGNED");
  await expect(page.locator("#hybrid-v2-predictions p")).toHaveCount(0);

  expect(externalRequests).toEqual([]);
  expect(pageErrors).toEqual([]);
  console.log(JSON.stringify({
    coldStartMs,
    warmStartMs,
    model: "byumatrixlab/lao-ipa-tonal",
    modelRevision: "e02608cfcb18abfe6b1916f5f4774bfac9ac788d",
    inference: "browser-local ONNX Runtime Web WASM",
    beamSize: 5,
    output: await ipa.textContent(),
    alignment: await alignment.textContent(),
    externalRequests,
  }, null, 2));
});

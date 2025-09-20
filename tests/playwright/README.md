# Playwright Scaffold (Disabled)

To enable only when UI/E2E required:
1) Install Node 20, then:
   npm init -y && npm i -D @playwright/test
2) Rename `mainFlow.spec.ts.disabled` → `mainFlow.spec.ts`
3) Add package.json scripts:
   "scripts": { "test": "playwright test", "lint": "eslint ." }
4) In CI, enable the test step (toggle the `if` condition).

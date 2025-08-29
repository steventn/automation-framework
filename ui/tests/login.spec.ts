import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { USERS } from '../fixtures/TestData';

test.describe('Login Tests', () => {
  test('Valid user can log in', async ({ page }) => {
    const { username, password } = USERS.validUser;
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login(username, password);
    await expect(page.locator('.header_label > .app_logo')).toHaveText('Swag Labs');
  });

  test('Invalid login shows error', async ({ page }) => {
    const { username, password } = USERS.invalidUser;
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login(username, password);
    await expect(page.locator('[data-test="error"]')).toBeVisible();
    await expect(page.locator('[data-test="error"]')).toHaveText('Epic sadface: Username and password do not match any user in this service')
  });
});

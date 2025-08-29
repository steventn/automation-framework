import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { USERS, MESSAGES } from '../fixtures/TestData';

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
    const { invalid_user_login_error } = MESSAGES;
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login(username, password);
    await expect(page.locator('[data-test="error"]')).toBeVisible();
    await expect(page.locator('[data-test="error"]')).toHaveText(invalid_user_login_error)
  });
});

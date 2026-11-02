// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import Login from "./Login";

afterEach(cleanup);

describe("sign-in preview", () => {
  it.each([
    ["Go back", /Sign in\/ Sign up/],
    ["Forgot your password?", "Go back"],
    ["Create account", "Go back"],
  ])("clears the password after leaving via %s", (exitLabel, returnLabel) => {
    render(<Login onPreview={() => {}} />);
    fireEvent.click(screen.getByRole("button", { name: /Sign in\/ Sign up/ }));
    fireEvent.change(screen.getByLabelText("Password *"), { target: { value: "private-password" } });
    fireEvent.click(screen.getByRole("button", { name: exitLabel }));
    fireEvent.click(screen.getByRole("button", { name: returnLabel, exact: false }));
    expect(screen.getByLabelText("Password *").value).toBe("");
  });
});

import "@testing-library/jest-dom/vitest";

import { cleanup } from "@testing-library/react";
import { afterEach } from "vitest";

if (typeof window !== "undefined") {
  class ResizeObserverMock {
    observe() {}

    unobserve() {}

    disconnect() {}
  }

  window.ResizeObserver = ResizeObserverMock;
  globalThis.ResizeObserver = ResizeObserverMock;
  window.HTMLElement.prototype.hasPointerCapture = () => false;
  window.HTMLElement.prototype.setPointerCapture = () => {};
  window.HTMLElement.prototype.releasePointerCapture = () => {};
  window.HTMLElement.prototype.scrollIntoView = () => {};
}

afterEach(cleanup);

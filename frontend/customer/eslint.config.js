import eslint from "@eslint/js";
import prettier from "eslint-config-prettier";
import globals from "globals";
import jsxA11y from "eslint-plugin-jsx-a11y";
import react from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";
import reactRefresh from "eslint-plugin-react-refresh";

export default [
  {
    ignores: [
      "artifacts/**",
      "coverage/",
      "dist/",
      "node_modules/",
      "operator-dashboard/**",
      "tmp/**",
    ],
  },
  {
    files: ["**/*.{js,jsx}"],
    languageOptions: {
      ecmaVersion: "latest",
      globals: {
        ...globals.browser,
        ...globals.node,
      },
      parserOptions: {
        ecmaFeatures: {
          jsx: true,
        },
        sourceType: "module",
      },
    },
    plugins: {
      "jsx-a11y": jsxA11y,
      react,
      "react-hooks": reactHooks,
      "react-refresh": reactRefresh,
    },
    rules: {
      ...eslint.configs.recommended.rules,
      ...react.configs.flat.recommended.rules,
      ...react.configs.flat["jsx-runtime"].rules,
      ...reactHooks.configs.flat["recommended-latest"].rules,
      ...reactRefresh.configs.vite.rules,
      ...jsxA11y.flatConfigs.recommended.rules,
      curly: ["error", "all"],
      eqeqeq: ["error", "always"],
      "no-console": ["warn", { allow: ["warn", "error"] }],
      "no-debugger": "error",
      "no-duplicate-imports": "error",
      "no-var": "error",
      "prefer-const": "error",
      "react/forbid-dom-props": ["error", { forbid: ["style"] }],
      "react/jsx-key": "error",
      "react/no-array-index-key": "error",
      "react/prop-types": "off",
      "react/self-closing-comp": "error",
    },
    settings: {
      react: {
        version: "detect",
      },
    },
  },
  {
    files: ["src/components/ui/**/*.{js,jsx}"],
    rules: {
      "react-refresh/only-export-components": "off",
    },
  },
  prettier,
];

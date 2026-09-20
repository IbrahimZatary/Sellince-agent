import { ArrowRightIcon, MessagesSquareIcon } from "lucide-react";
import { useState } from "react";
import { useNavigate } from "react-router";
import { useAuth } from "@/components/auth/AuthContext";

import sellinceAssistantProduct from "@/assets/images/sellince-assistant-product.png";
import sellinceIntelligenceProduct from "@/assets/images/sellince-intelligence-product.png";
import OnboardingHeader from "@/components/onboarding/OnboardingHeader";
import OnboardingProgress from "@/components/onboarding/OnboardingProgress";
import ProductSelectionCard from "@/components/onboarding/ProductSelectionCard";
import { Button } from "@/components/ui/button";

/**
 * Available Sellince products offered during onboarding workspace setup.
 */
const ONBOARDING_PRODUCTS = [
  {
    productId: "ai-sales-assistant",
    productNumber: "01",
    productName: "AI Sales Assistant",
    productDescription:
      "Start relevant customer conversations and guide every customer toward the right offer.",
    actionLabel: "Continue with Assistant",
    destinationRoute: "/chat",
    illustrationSource: sellinceAssistantProduct,
    illustrationAlt: "",
    isAvailable: true,
  },
  {
    productId: "opportunity-intelligence",
    productNumber: "02",
    productName: "Opportunity Intelligence",
    productDescription: "Explore customer signals and identify the strongest sales opportunities.",
    actionLabel: "Open Intelligence",
    destinationRoute: null,
    illustrationSource: sellinceIntelligenceProduct,
    illustrationAlt: "",
    isAvailable: false,
  },
];

const DEFAULT_PRODUCT_ID = "ai-sales-assistant";
const INTELLIGENCE_UNAVAILABLE_MESSAGE =
  "Opportunity Intelligence is being prepared and will be available soon.";

/**
 * Onboarding Page
 *
 * Directs newly registered users through the workspace onboarding flow:
 * 1. Shows progress tracker (`ACCOUNT CREATED` -> `CHOOSE WORKSPACE` -> `START`).
 * 2. Presents interactive product selection cards for Sellince modules.
 * 3. Navigates to `/chat` upon selecting the active AI Sales Assistant product.
 */
function Onboarding() {
  const navigate = useNavigate();
  const { signOut } = useAuth();
  const [selectedProductId, setSelectedProductId] = useState(DEFAULT_PRODUCT_ID);
  const [productActionMessage, setProductActionMessage] = useState("");

  function handleProductSelect(productId) {
    setSelectedProductId(productId);
    setProductActionMessage("");
  }

  function handleProductAction(productId) {
    const chosenProduct = ONBOARDING_PRODUCTS.find((product) => product.productId === productId);

    if (!chosenProduct) {
      return;
    }

    setSelectedProductId(productId);

    if (chosenProduct.isAvailable && chosenProduct.destinationRoute) {
      navigate(chosenProduct.destinationRoute);
      return;
    }

    setProductActionMessage(INTELLIGENCE_UNAVAILABLE_MESSAGE);
  }

  async function handleSignOut() {
    await signOut();
    navigate("/login", { replace: true });
  }

  function handleCompareServices() {
    setProductActionMessage("Review the two product descriptions above to compare services.");
  }

  return (
    <div className="bg-background text-foreground relative min-h-dvh overflow-x-hidden">
      <OnboardingHeader accountLabel="Account" accountInitials="U" onSignOut={handleSignOut} />

      <img
        src={sellinceIntelligenceProduct}
        alt=""
        aria-hidden="true"
        className="pointer-events-none absolute top-20 -right-80 hidden w-180 opacity-10 lg:block"
      />
      <img
        src={sellinceAssistantProduct}
        alt=""
        aria-hidden="true"
        className="pointer-events-none absolute -bottom-48 -left-96 hidden w-180 opacity-10 lg:block"
      />

      <main className="relative mx-auto max-w-7xl px-5 pt-8 pb-8 md:px-8 md:pt-10 lg:pt-10">
        <OnboardingProgress />

        <section className="mt-10 md:mt-9" aria-labelledby="onboarding-title">
          <p className="text-primary tracking-label text-xs font-semibold sm:text-sm">
            SELECT YOUR WORKSPACE
          </p>
          <h1
            id="onboarding-title"
            className="mt-3 max-w-4xl text-4xl leading-tight font-semibold tracking-tight md:text-5xl"
          >
            How would you like Sellince to help?
          </h1>
          <p className="text-muted-foreground mt-2 text-base sm:text-lg">
            Choose a service to continue. You can switch workspaces later.
          </p>

          <fieldset className="mt-7">
            <legend className="sr-only">Choose a Sellince workspace</legend>
            <div className="grid items-stretch gap-5 md:grid-cols-2 lg:gap-7">
              {ONBOARDING_PRODUCTS.map((product) => (
                <ProductSelectionCard
                  key={product.productId}
                  {...product}
                  isSelected={selectedProductId === product.productId}
                  onProductSelect={handleProductSelect}
                  onProductAction={handleProductAction}
                />
              ))}
            </div>
          </fieldset>

          <div className="mt-6 grid gap-4 text-sm md:grid-cols-3 md:items-center">
            <p className="text-muted-foreground flex items-center gap-2">
              <MessagesSquareIcon className="size-4" aria-hidden="true" />
              Need help choosing?
            </p>
            <p className="text-muted-foreground md:text-center">
              Your selection can be changed from workspace settings.
            </p>
            <Button
              type="button"
              variant="link"
              className="h-auto justify-start p-0 md:justify-end"
              onClick={handleCompareServices}
            >
              Compare services
              <ArrowRightIcon data-icon="inline-end" />
            </Button>
          </div>

          <p className="text-muted-foreground mt-3 min-h-5 text-center text-sm" role="status">
            {productActionMessage}
          </p>
        </section>
      </main>
    </div>
  );
}

export default Onboarding;

import { useSearchParams } from "react-router";
import { useState } from "react";
import { completeCheckout } from "@/api/chat.api";

function Checkout() {
  const [searchParams] = useSearchParams();
  const customerId = searchParams.get("customer_id") || "unknown";
  const conversationId = searchParams.get("conversation_id") || "unknown";
  const productId = searchParams.get("product_id") || "unknown";
  const productName = searchParams.get("product_name") || "Selected plan";
  const price = searchParams.get("price") || "25.00";
  const attributionId = searchParams.get("attribution_id");
  const [status, setStatus] = useState("idle");
  const [paymentInfo, setPaymentInfo] = useState({
    name: "",
    cardNumber: "",
    expiry: "",
    cvv: "",
  });

  const updatePaymentInfo = (event) => {
    setPaymentInfo((current) => ({
      ...current,
      [event.target.name]: event.target.value,
    }));
  };

  const handlePay = async (event) => {
    event.preventDefault();
    setStatus("loading");
    try {
      await completeCheckout({
        customer_id: Number(customerId),
        conversation_id: Number(conversationId),
        product_id: productId,
      });
      setStatus("success");
    } catch {
      setStatus("error");
    }
  };

  return (
    <main className="bg-background flex min-h-dvh items-center justify-center p-4 sm:p-6">
      <div className="bg-card border-border w-full max-w-md rounded-2xl border p-6 shadow-lg sm:p-8">
        {status === "success" ? (
          <div className="py-8 text-center">
            <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-green-100 text-xl text-green-700">
              ✓
            </div>
            <h1 className="text-foreground mt-5 text-2xl font-semibold">Payment confirmed</h1>
            <p className="text-muted-foreground mt-2 text-sm">
              Your {productName} plan is now active.
            </p>
            <button
              type="button"
              className="border-border text-foreground mt-6 w-full rounded-xl border px-4 py-3 font-medium"
              onClick={() => window.history.back()}
            >
              Return to chat
            </button>
          </div>
        ) : (
          <>
            <p className="text-muted-foreground text-sm font-medium">Sellince</p>
            <h1 className="text-foreground mt-2 text-3xl font-semibold">Complete your purchase</h1>
            <p className="text-muted-foreground mt-2 text-sm">
              Review your plan and enter your payment details.
            </p>

            <div className="border-border bg-background mt-6 flex items-center justify-between gap-4 rounded-xl border p-4">
              <div>
                <p className="text-muted-foreground text-xs tracking-wide uppercase">
                  Selected plan
                </p>
                <p className="text-foreground mt-1 font-semibold">{productName}</p>
              </div>
              <p className="text-foreground shrink-0 text-lg font-semibold">
                {Number(price).toFixed(2)} JOD
              </p>
            </div>

            <form className="mt-6 space-y-4" onSubmit={handlePay}>
              <div className="space-y-1">
                <label className="text-foreground text-sm font-medium" htmlFor="name">
                  Name on card
                </label>
                <input
                  id="name"
                  name="name"
                  value={paymentInfo.name}
                  onChange={updatePaymentInfo}
                  autoComplete="cc-name"
                  required
                  className="border-border bg-background text-foreground w-full rounded-lg border px-3 py-2"
                />
              </div>
              <div className="space-y-1">
                <label className="text-foreground text-sm font-medium" htmlFor="cardNumber">
                  Card number
                </label>
                <input
                  id="cardNumber"
                  name="cardNumber"
                  value={paymentInfo.cardNumber}
                  onChange={updatePaymentInfo}
                  inputMode="numeric"
                  autoComplete="cc-number"
                  pattern="[0-9 ]{12,19}"
                  maxLength={19}
                  placeholder="4242 4242 4242 4242"
                  required
                  className="border-border bg-background text-foreground w-full rounded-lg border px-3 py-2"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="space-y-1">
                  <label className="text-foreground text-sm font-medium" htmlFor="expiry">
                    Expiry
                  </label>
                  <input
                    id="expiry"
                    name="expiry"
                    value={paymentInfo.expiry}
                    onChange={updatePaymentInfo}
                    placeholder="MM/YY"
                    autoComplete="cc-exp"
                    pattern="(0[1-9]|1[0-2])/[0-9]{2}"
                    required
                    className="border-border bg-background text-foreground w-full rounded-lg border px-3 py-2"
                  />
                </div>
                <div className="space-y-1">
                  <label className="text-foreground text-sm font-medium" htmlFor="cvv">
                    Security code
                  </label>
                  <input
                    id="cvv"
                    name="cvv"
                    value={paymentInfo.cvv}
                    onChange={updatePaymentInfo}
                    inputMode="numeric"
                    autoComplete="cc-csc"
                    pattern="[0-9]{3,4}"
                    maxLength={4}
                    required
                    className="border-border bg-background text-foreground w-full rounded-lg border px-3 py-2"
                  />
                </div>
              </div>
              <p className="text-muted-foreground text-xs">
                Demo only: your details are not sent to a payment provider.
              </p>
              <button
                type="submit"
                className="bg-primary text-primary-foreground w-full rounded-xl px-4 py-3 font-medium"
                disabled={status === "loading" || !attributionId}
              >
                {status === "loading"
                  ? "Processing..."
                  : status === "success"
                    ? "Payment complete"
                    : "Pay now"}
              </button>
              {status === "error" ? (
                <p className="text-center text-sm text-red-700">
                  This checkout could not be completed.
                </p>
              ) : null}
              <button
                type="button"
                className="border-border text-foreground w-full rounded-xl border px-4 py-3 font-medium"
                onClick={() => window.history.back()}
              >
                Back to chat
              </button>
            </form>
          </>
        )}
      </div>
    </main>
  );
}

export default Checkout;

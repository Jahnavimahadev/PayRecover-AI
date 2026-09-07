print("========================================")
print("          PAYRECOVER AI")
print("   Intelligent Revenue Recovery Agent")
print("========================================")

customer = input("\nEnter customer name: ")
amount = float(input("Enter payment amount: ₹"))
reason = input(
    "Enter failure reason "
    "(temporary/insufficient_funds/expired_card/other): "
).lower()

attempts = int(input("Enter previous retry attempts: "))

print("\nAnalyzing payment...")
print("----------------------------------------")

# Recovery decision engine
if reason == "temporary":
    if attempts == 0:
        action = "RETRY"
        explanation = "Temporary failure with no previous retry."
    elif attempts == 1:
        action = "RETRY"
        explanation = "Temporary failure; one controlled retry remains."
    else:
        action = "ESCALATE"
        explanation = "Retry limit reached."

elif reason == "insufficient_funds":
    action = "REMINDER"
    explanation = "Customer may need to add funds before retrying."

elif reason == "expired_card":
    action = "UPDATE PAYMENT METHOD"
    explanation = "The payment method appears to be expired."

else:
    action = "ESCALATE"
    explanation = "Failure reason requires further review."

print("\nCUSTOMER:", customer)
print("AMOUNT: ₹", amount)
print("FAILURE REASON:", reason)
print("PREVIOUS ATTEMPTS:", attempts)

print("\n🤖 PAYRECOVER AI DECISION")
print("ACTION:", action)
print("REASON:", explanation)

if action == "RETRY":
    print("✅ Controlled payment retry recommended.")

elif action == "REMINDER":
    print("📩 Send payment reminder to customer.")

elif action == "UPDATE PAYMENT METHOD":
    print("💳 Ask customer to update payment method.")

else:
    print("🛑 Stop automatic retries and escalate.")

print("\nRevenue recovery analysis completed.")
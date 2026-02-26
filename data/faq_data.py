# =============================================================================
# FAQ DATA — Database for FAQ Assistant
# =============================================================================
# - Simulates a realistic FAQ database that contains FAQs for answering customer questions

FAQ_DATA = [

    # ── ACCOUNT (4 entries) ────────────────────────────────────────────
    {
        "question": "How do I reset my password?",
        "answer": "Click 'Forgot Password' on the login page. "
                  "You will receive an email with a reset link. "
                  "The link is valid for 24 hours.",
        "category": "account",
        "source": "faq",
    },
    {
        "question": "How do I change my email address?",
        "answer": "Go to Settings > Profile > Change Email. "
                  "A confirmation link will be sent to the new address.",
        "category": "account",
        "source": "faq",
    },
    {
        "question": "How do I change my username?",
        "answer": "Go to Settings > Profile > Username. "
                  "Your username can be changed once every 30 days.",
        "category": "account",
        "source": "faq",
    },
    {
        "question": "How do I delete my account?",
        "answer": "Go to Settings > Account > Delete Account. "
                  "Please note that this action is permanent and cannot be undone. "
                  "Your data will be removed within 30 days.",
        "category": "account",
        "source": "faq",
    },

    # ── PRICE (4 entries) ─────────────────────────────────────────────
    {
        "question": "How much does the Premium subscription cost?",
        "answer": "The Premium subscription costs €9.99 per month "
                  "or €99 per year (2 months free).",
        "category": "price",
        "source": "faq",
    },
    {
        "question": "Is there a free trial?",
        "answer": "Yes, we offer a 14-day free trial. "
                  "No credit card required.",
        "category": "price",
        "source": "faq",
    },
    {
        "question": "Is there a student discount?",
        "answer": "Yes, students receive a 30% discount with a valid "
                  "university email address. "
                  "Apply via Settings > Billing > Student Discount.",
        "category": "price",
        "source": "faq",
    },
    {
        "question": "What happens when my free trial ends?",
        "answer": "Your account will automatically switch to the free "
                  "plan. No charges will be made without your consent. "
                  "You can upgrade at any time in Settings > Billing.",
        "category": "price",
        "source": "faq",
    },

    # ── SUBSCRIPTION (4 entries) ──────────────────────────────────────
    {
        "question": "How do I cancel my subscription?",
        "answer": "Go to Settings > Subscription > Cancel. "
                  "Cancellation takes effect at the end of the current billing period.",
        "category": "subscription",
        "source": "faq",
    },
    {
        "question": "Can I pause my subscription?",
        "answer": "Yes, for up to 3 months. "
                  "Go to Settings > Subscription > Pause.",
        "category": "subscription",
        "source": "faq",
    },
    {
        "question": "Can I upgrade my subscription plan?",
        "answer": "Yes, go to Settings > Subscription > Upgrade. "
                  "The price difference will be charged on a pro-rata basis "
                  "for the remaining billing period.",
        "category": "subscription",
        "source": "faq",
    },
    {
        "question": "Can I switch from monthly to yearly billing?",
        "answer": "Yes, go to Settings > Subscription > Billing Cycle. "
                  "Switching to yearly saves you the equivalent of 2 months. "
                  "The change takes effect at the next renewal date.",
        "category": "subscription",
        "source": "faq",
    },

    # ── SUPPORT (4 entries) ───────────────────────────────────────────
    {
        "question": "How do I contact customer support?",
        "answer": "Email: support@example.com or Phone: 0800-123456 "
                  "(Mon–Fri, 9am–6pm).",
        "category": "support",
        "source": "faq",
    },
    {
        "question": "What are your customer support hours?",
        "answer": "Our support team is available Monday to Friday, "
                  "9am to 6pm CET. "
                  "For urgent issues outside these hours, please use our help center.",
        "category": "support",
        "source": "faq",
    },
    {
        "question": "How long does it take to receive a support response?",
        "answer": "We aim to respond to all inquiries within 24 hours "
                  "on business days. "
                  "Priority support is available for Premium subscribers.",
        "category": "support",
        "source": "faq",
    },
    {
        "question": "Where can I find answers to common questions?",
        "answer": "Our Help Center at help.example.com contains "
                  "articles and guides for the most common topics. "
                  "You can also use the search bar to find specific answers.",
        "category": "support",
        "source": "faq",
    },

    # ── PAYMENT (4 entries) ───────────────────────────────────────────
    {
        "question": "Which payment methods are accepted?",
        "answer": "We accept credit cards (Visa, Mastercard), "
                  "PayPal, and SEPA direct debit.",
        "category": "payment",
        "source": "faq",
    },
    {
        "question": "Can I get a refund?",
        "answer": "Refunds are available within 14 days of purchase "
                  "if the service has not been used. "
                  "Please contact support@example.com with your order details.",
        "category": "payment",
        "source": "faq",
    },
    {
        "question": "How do I request an invoice?",
        "answer": "Invoices are generated automatically after each payment "
                  "and sent to your billing email address. "
                  "You can also download past invoices via Settings > Billing > Invoice History.",
        "category": "payment",
        "source": "faq",
    },
    {
        "question": "How do I update my billing address?",
        "answer": "Go to Settings > Billing > Billing Address. "
                  "Changes will apply to all future invoices. "
                  "Past invoices cannot be modified.",
        "category": "payment",
        "source": "faq",
    },

    # ── FEEDBACK (4 entries) ──────────────────────────────────────────
    {
        "question": "How do I submit a feature request?",
        "answer": "We love hearing your ideas! "
                  "Submit feature requests via Settings > Feedback > Feature Request. "
                  "Popular requests are reviewed by our product team each month.",
        "category": "feedback",
        "source": "faq",
    },
    {
        "question": "How do I report a bug?",
        "answer": "Please report bugs via Settings > Feedback > Report a Bug. "
                  "Include a description of the issue and the steps to reproduce it. "
                  "Screenshots are helpful but not required.",
        "category": "feedback",
        "source": "faq",
    },
    {
        "question": "Can I rate my support experience?",
        "answer": "Yes, after each support interaction you will receive "
                  "a short satisfaction survey by email. "
                  "Your feedback helps us improve our service.",
        "category": "feedback",
        "source": "faq",
    },
    {
        "question": "Is there a community forum where I can share feedback?",
        "answer": "Yes, our community forum is available at community.example.com. "
                  "You can share ideas, report issues, and vote on feature requests "
                  "submitted by other users.",
        "category": "feedback",
        "source": "faq",
    },

]

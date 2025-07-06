import pandas as pd
import json
from datetime import datetime, timedelta
import random

# Sample customer support tickets dataset
def create_sample_tickets_dataset():
    """
    Creates a comprehensive sample dataset of customer support tickets
    for training and testing the RAG-based support system.
    """
    
    # Define ticket categories and their typical issues
    ticket_categories = {
        'Shipping': [
            'Order not delivered',
            'Package damaged during shipping',
            'Wrong delivery address',
            'Delayed shipment',
            'Missing items from order',
            'Tracking number not working',
            'Package lost in transit',
            'Delivery to wrong address'
        ],
        'Returns': [
            'Want to return item',
            'Defective product received',
            'Item not as described',
            'Wrong size/color received',
            'Return policy inquiry',
            'Return shipping label request',
            'Refund status inquiry',
            'Exchange request'
        ],
        'Payment': [
            'Payment failed but money deducted',
            'Credit card charged twice',
            'Refund not received',
            'Payment method declined',
            'Billing address issue',
            'Promotional code not working',
            'Subscription billing problem',
            'Transaction dispute'
        ],
        'Product': [
            'Product not working',
            'Installation help needed',
            'Warranty claim',
            'Product specifications inquiry',
            'Compatibility question',
            'User manual request',
            'Product recommendation',
            'Feature request'
        ],
        'Account': [
            'Cannot login to account',
            'Forgot password',
            'Account locked',
            'Profile update needed',
            'Email not receiving',
            'Account deletion request',
            'Privacy settings',
            'Two-factor authentication'
        ],
        'General': [
            'Website not loading',
            'General inquiry',
            'Feedback about service',
            'Contact information update',
            'Store hours inquiry',
            'Complaint about service',
            'Suggestion for improvement',
            'Partnership inquiry'
        ]
    }
    
    # Sample customer descriptions with varying complexity
    ticket_descriptions = {
        'Shipping': [
            "I ordered a laptop 5 days ago but it hasn't arrived yet. The tracking shows it's still in transit. When will I receive it?",
            "My package arrived but the box was completely damaged and the product inside is broken. I need a replacement urgently.",
            "I moved to a new address after placing my order. Can you change the delivery address before it ships?",
            "My order was supposed to arrive yesterday but the tracking hasn't updated in 3 days. Is it lost?",
            "I received my order but it's missing the charger that was supposed to be included. Order #12345",
            "The tracking number you provided doesn't work on any shipping website. Can you help me track my package?",
            "I've been waiting for 2 weeks and my package still hasn't arrived. This is unacceptable for express shipping.",
            "My package was delivered to the wrong address. The neighbor brought it over but this shouldn't happen."
        ],
        'Returns': [
            "I want to return this sweater because it doesn't fit properly. It's too small even though I ordered the right size.",
            "The phone I received is clearly defective - it won't turn on and the screen is cracked. I need a full refund.",
            "The product description said it was waterproof but it's clearly not. I want to return it for false advertising.",
            "I ordered a red shirt but received a blue one. Can I exchange it for the correct color?",
            "What's your return policy? I bought something last month and want to know if I can still return it.",
            "I need a return shipping label for my recent purchase. The product arrived damaged.",
            "I submitted a return request last week but haven't received my refund yet. When will I get my money back?",
            "Can I exchange this item for a different size? I have the original receipt and packaging."
        ],
        'Payment': [
            "My payment failed during checkout but my bank account was charged. I need this resolved immediately.",
            "I was charged twice for the same order. Please refund the duplicate charge to my credit card.",
            "I returned an item 3 weeks ago but still haven't received my refund. This is taking too long.",
            "My credit card was declined even though I have sufficient funds. What's the problem?",
            "There's an error with my billing address and I can't complete my purchase. How do I fix this?",
            "The discount code SAVE20 isn't working at checkout. It should give me 20% off my order.",
            "I'm being charged for a subscription I cancelled last month. Please stop these charges.",
            "I want to dispute a charge on my account. The transaction doesn't look legitimate."
        ],
        'Product': [
            "My new printer isn't working properly. It keeps jamming and the print quality is poor.",
            "I need help installing the software that came with my new computer. The instructions are confusing.",
            "My product broke after just 2 weeks of use. Is this covered under warranty?",
            "Can you tell me the exact dimensions of the large size backpack? I need to know if it fits my laptop.",
            "Is this wireless mouse compatible with Mac computers? The product page doesn't specify.",
            "I lost the user manual for my device. Can you email me a digital copy?",
            "I'm looking for a good laptop for gaming. What would you recommend from your current selection?",
            "It would be great if you could add a dark mode feature to your mobile app. Many users would appreciate it."
        ],
        'Account': [
            "I can't log into my account. I keep getting an error message saying invalid credentials.",
            "I forgot my password and the reset email isn't coming through. I've checked my spam folder.",
            "My account has been locked after too many failed login attempts. How do I unlock it?",
            "I need to update my profile information but can't find the option in my account settings.",
            "I'm not receiving promotional emails anymore. I want to make sure I'm still subscribed.",
            "I want to permanently delete my account and all associated data. How do I do this?",
            "How do I change my privacy settings? I don't want my purchase history to be visible.",
            "I'm having trouble setting up two-factor authentication. The app isn't recognizing the QR code."
        ],
        'General': [
            "Your website keeps crashing when I try to browse products. This is very frustrating.",
            "I just wanted to say thank you for your excellent customer service. The representative was very helpful.",
            "I have a general question about your company's sustainability practices. Do you use eco-friendly packaging?",
            "I need to update my contact information but can't find where to do it on the website.",
            "What are your store hours? I want to visit your physical location this weekend.",
            "I'm very disappointed with my recent purchase experience. The product quality has declined significantly.",
            "I have a suggestion for your website - it would be helpful to have a live chat feature.",
            "I'm interested in becoming a business partner. Who should I contact about wholesale opportunities?"
        ]
    }
    
    # Sample resolutions for each category
    ticket_resolutions = {
        'Shipping': [
            "Contacted shipping carrier and expedited delivery. Package will arrive within 2 business days.",
            "Arranged immediate replacement shipment. Original damaged package return label provided.",
            "Updated delivery address in system. Package will be redirected to new address.",
            "Tracked package location and confirmed delivery for next business day.",
            "Processed replacement for missing item. Expedited shipping at no charge.",
            "Provided correct tracking information and carrier details for package monitoring.",
            "Initiated trace request with carrier and arranged replacement shipment.",
            "Confirmed delivery address and provided instructions to prevent future issues."
        ],
        'Returns': [
            "Provided return label and processed refund upon receipt of returned item.",
            "Arranged immediate replacement shipment and return label for defective item.",
            "Processed full refund and return label. Quality team notified of description issue.",
            "Initiated exchange process for correct color. Return label provided.",
            "Confirmed 30-day return policy applies. Return label provided for eligible item.",
            "Emailed return shipping label and provided tracking information.",
            "Refund processed successfully. Amount will appear in account within 3-5 business days.",
            "Exchange approved. Return label sent and replacement will ship upon receipt."
        ],
        'Payment': [
            "Identified duplicate charge and processed refund. Amount will appear within 24 hours.",
            "Confirmed duplicate charge and initiated refund process to original payment method.",
            "Located return processing delay and expedited refund. Completed within 48 hours.",
            "Identified payment processor issue and provided alternative payment method.",
            "Updated billing address in system and confirmed payment processing.",
            "Validated discount code and applied to order. Refund processed for difference.",
            "Cancelled subscription and processed refund for current billing period.",
            "Initiated dispute investigation and temporarily credited account pending resolution."
        ],
        'Product': [
            "Diagnosed printer issue and provided troubleshooting steps. Replacement arranged if needed.",
            "Provided step-by-step installation guide and remote support session scheduled.",
            "Confirmed warranty coverage and arranged replacement shipment at no charge.",
            "Provided detailed product specifications and sizing guide for reference.",
            "Confirmed Mac compatibility and provided setup instructions for optimal performance.",
            "Emailed digital user manual and created account access for future reference.",
            "Provided personalized gaming laptop recommendations based on requirements and budget.",
            "Forwarded feature request to development team and provided timeline for updates."
        ],
        'Account': [
            "Reset account credentials and provided temporary password for immediate access.",
            "Manually triggered password reset and confirmed email delivery to correct address.",
            "Unlocked account and provided security tips to prevent future lockouts.",
            "Guided through profile update process and confirmed all changes saved successfully.",
            "Verified email preferences and re-subscribed to promotional communications.",
            "Processed account deletion request and confirmed all data removed within 48 hours.",
            "Updated privacy settings and provided overview of available options.",
            "Provided alternative 2FA setup method and confirmed successful activation."
        ],
        'General': [
            "Identified website performance issue and escalated to technical team for immediate resolution.",
            "Forwarded positive feedback to service team and offered additional assistance.",
            "Provided detailed information about sustainability practices and eco-friendly initiatives.",
            "Guided through contact information update process and confirmed changes saved.",
            "Provided store hours and location information with directions and contact details.",
            "Escalated quality concern to management and offered resolution options.",
            "Forwarded website improvement suggestion to development team for consideration.",
            "Connected with business development team and provided partnership application process."
        ]
    }
    
    # Priority levels and their criteria
    priority_levels = ['Low', 'Medium', 'High', 'Critical']
    priority_weights = [0.4, 0.3, 0.2, 0.1]  # Distribution of priorities
    
    # Status options
    status_options = ['Open', 'In Progress', 'Resolved', 'Closed']
    status_weights = [0.1, 0.2, 0.5, 0.2]
    
    # Sample customer names and emails
    customer_names = [
        'John Smith', 'Sarah Johnson', 'Mike Davis', 'Lisa Wilson', 'David Brown',
        'Emma Thompson', 'James Miller', 'Anna Garcia', 'Robert Taylor', 'Maria Rodriguez',
        'Chris Anderson', 'Jennifer White', 'Mark Johnson', 'Amy Chen', 'Steve Wilson',
        'Laura Martinez', 'Paul Davis', 'Jessica Lee', 'Kevin Brown', 'Rachel Green'
    ]
    
    # Generate sample tickets
    tickets = []
    ticket_id = 1000
    
    for category, issues in ticket_categories.items():
        for i in range(15):  # 15 tickets per category = 90 total tickets
            # Select random issue and description
            issue_idx = random.randint(0, len(issues) - 1)
            issue = issues[issue_idx]
            description = ticket_descriptions[category][issue_idx]
            
            # Generate customer info
            customer_name = random.choice(customer_names)
            customer_email = f"{customer_name.lower().replace(' ', '.')}.{random.randint(100, 999)}@email.com"
            
            # Generate timestamps
            created_date = datetime.now() - timedelta(days=random.randint(1, 30))
            if random.random() > 0.3:  # 70% chance of being updated
                updated_date = created_date + timedelta(hours=random.randint(1, 72))
            else:
                updated_date = created_date
            
            # Assign priority and status
            priority = random.choices(priority_levels, weights=priority_weights)[0]
            status = random.choices(status_options, weights=status_weights)[0]
            
            # Add resolution if status is Resolved or Closed
            resolution = ""
            if status in ['Resolved', 'Closed']:
                resolution = random.choice(ticket_resolutions[category])
            
            # Create ticket
            ticket = {
                'ticket_id': f"TK-{ticket_id}",
                'title': issue,
                'description': description,
                'category': category,
                'priority': priority,
                'status': status,
                'customer_name': customer_name,
                'customer_email': customer_email,
                'created_date': created_date.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_date': updated_date.strftime('%Y-%m-%d %H:%M:%S'),
                'resolution': resolution,
                'agent_assigned': f"Agent_{random.randint(1, 10)}" if status != 'Open' else "",
                'tags': f"{category.lower()}, {priority.lower()}",
                'customer_satisfaction': random.choice([3, 4, 5]) if status == 'Closed' else None
            }
            
            tickets.append(ticket)
            ticket_id += 1
    
    return tickets

# Create the dataset
def save_dataset():
    """Save the dataset in multiple formats for different use cases"""
    
    tickets = create_sample_tickets_dataset()
    
    # Save as CSV
    df = pd.DataFrame(tickets)
    df.to_csv('customer_support_tickets.csv', index=False)
    print(f"Saved {len(tickets)} tickets to customer_support_tickets.csv")
    
    # Save as JSON for API use
    with open('customer_support_tickets.json', 'w') as f:
        json.dump(tickets, f, indent=2)
    print(f"Saved {len(tickets)} tickets to customer_support_tickets.json")
    
    # Create summary statistics
    df_summary = df.groupby(['category', 'priority', 'status']).size().reset_index(name='count')
    print("\nDataset Summary:")
    print(df_summary.to_string(index=False))
    
    # Category distribution
    print("\nCategory Distribution:")
    print(df['category'].value_counts().to_string())
    
    # Priority distribution
    print("\nPriority Distribution:")
    print(df['priority'].value_counts().to_string())
    
    # Status distribution
    print("\nStatus Distribution:")
    print(df['status'].value_counts().to_string())
    
    return df

# Company Knowledge Base
def create_company_knowledge_base():
    """Create a sample company knowledge base for RAG system"""
    
    knowledge_base = {
        'policies': {
            'return_policy': {
                'title': 'Return Policy',
                'content': """
                Our return policy allows customers to return most items within 30 days of purchase 
                for a full refund. Items must be in original condition with all packaging and tags 
                intact. Electronics must be returned within 14 days due to their nature. 
                Custom or personalized items cannot be returned unless defective.
                
                To initiate a return:
                1. Log into your account and go to Order History
                2. Select the item you wish to return
                3. Print the prepaid return label
                4. Package the item securely and attach the label
                5. Drop off at any authorized shipping location
                
                Refunds are processed within 3-5 business days after we receive the returned item.
                """
            },
            'shipping_policy': {
                'title': 'Shipping Policy',
                'content': """
                We offer several shipping options:
                - Standard Shipping (5-7 business days): Free on orders over $50
                - Express Shipping (2-3 business days): $9.99
                - Overnight Shipping (1 business day): $19.99
                
                Orders placed before 2 PM EST ship the same day. We ship Monday through Friday.
                Weekend orders are processed on the following Monday.
                
                We ship to all 50 states and offer international shipping to select countries.
                Tracking information is provided via email once your order ships.
                """
            },
            'warranty_policy': {
                'title': 'Warranty Policy',
                'content': """
                All products come with a manufacturer's warranty. Warranty periods vary by product:
                - Electronics: 1-2 years depending on manufacturer
                - Appliances: 1-3 years depending on type
                - Clothing: 90 days for defects in materials or workmanship
                - Accessories: 6 months to 1 year
                
                Warranty claims require proof of purchase and must be reported within the warranty period.
                We facilitate warranty claims directly with manufacturers to ensure quick resolution.
                """
            }
        },
        'products': {
            'laptops': {
                'title': 'Laptop Information',
                'content': """
                We carry a wide selection of laptops from top brands including Dell, HP, Lenovo, 
                Apple, and ASUS. Our laptops range from budget-friendly options under $500 to 
                high-end gaming and professional workstations over $3000.
                
                Popular categories:
                - Business Laptops: Professional grade with long battery life
                - Gaming Laptops: High-performance graphics and processors
                - Ultrabooks: Thin, light, and portable for travel
                - 2-in-1 Convertibles: Laptop and tablet functionality
                
                All laptops come with a 1-year manufacturer warranty and 30-day return policy.
                """
            },
            'smartphones': {
                'title': 'Smartphone Information',
                'content': """
                We offer the latest smartphones from Apple, Samsung, Google, and other leading brands.
                All phones are unlocked and compatible with major carriers.
                
                Features to consider:
                - Operating System: iOS vs Android
                - Storage: 64GB to 1TB options available
                - Camera: Single, dual, or triple camera systems
                - Battery Life: All-day battery on most models
                - 5G Compatibility: Available on newer models
                
                Trade-in programs available for qualifying devices.
                """
            }
        },
        'faqs': {
            'payment_methods': {
                'title': 'Accepted Payment Methods',
                'content': """
                We accept the following payment methods:
                - Credit Cards: Visa, MasterCard, American Express, Discover
                - Debit Cards: With Visa or MasterCard logos
                - PayPal: Including PayPal Credit
                - Apple Pay: For mobile and online purchases
                - Google Pay: For mobile and online purchases
                - Gift Cards: Store gift cards and promotional codes
                
                We use secure encryption for all transactions and never store your payment information.
                """
            },
            'account_help': {
                'title': 'Account Help',
                'content': """
                Creating an account allows you to:
                - Track orders and view order history
                - Save items to your wishlist
                - Store multiple shipping addresses
                - Access exclusive member deals
                - Manage your communication preferences
                
                Forgot your password? Use the "Forgot Password" link on the login page.
                Your account will be temporarily locked after 5 failed login attempts for security.
                """
            }
        }
    }
    
    # Save knowledge base
    with open('company_knowledge_base.json', 'w') as f:
        json.dump(knowledge_base, f, indent=2)
    print("Saved company knowledge base to company_knowledge_base.json")
    
    return knowledge_base

# Main execution
if __name__ == "__main__":
    # Create and save the tickets dataset
    df = save_dataset()
    
    # Create and save the knowledge base
    kb = create_company_knowledge_base()
    
    print("\n" + "="*50)
    print("DATASET CREATION COMPLETE")
    print("="*50)
    print("Files created:")
    print("- customer_support_tickets.csv (for analysis)")
    print("- customer_support_tickets.json (for API)")
    print("- company_knowledge_base.json (for RAG system)")
    print("\nYou can now use these files to train and test your RAG system!")
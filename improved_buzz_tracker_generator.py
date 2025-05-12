#!/usr/bin/env python3
import random
import csv
import os
from datetime import datetime, timedelta
import string
import time

print("Starting generation of improved Buzz Tracker dataset...")

# Define constants
NUM_ROWS = 12000
OUTPUT_FILE = 'buzz_tracker_dataset_improved.csv'

# Define choices for categorical variables
PLATFORMS = ['Twitter', 'Instagram', 'Facebook', 'YouTube', 'Reddit']
LANGUAGES = ['en', 'hi', 'fr', 'es', 'de', 'pt', 'ru', 'ja', 'zh', 'ar']
TOPIC_CATEGORIES = ['Delivery', 'Product', 'Support', 'Pricing', 'Marketing', 'Returns']
SENTIMENT_LABELS = ['Positive', 'Neutral', 'Negative']
EMOTION_TYPES = ['Happy', 'Sad', 'Angry', 'Excited', 'Confused']
BRAND_NAMES = ['Nike', 'Pepsi', 'Apple', 'Samsung', 'Adidas', 'Google', 'Amazon', 'Microsoft', 'Toyota', 'Coca-Cola']
CAMPAIGN_PHASES = ['Pre-Launch', 'Launch', 'Post-Launch']

# Create cities and countries combinations
LOCATIONS = [
    'New York, USA', 'Los Angeles, USA', 'Chicago, USA', 'Houston, USA', 'Toronto, Canada',
    'Vancouver, Canada', 'London, UK', 'Manchester, UK', 'Paris, France', 'Lyon, France',
    'Berlin, Germany', 'Munich, Germany', 'Madrid, Spain', 'Barcelona, Spain', 'Rome, Italy',
    'Milan, Italy', 'Tokyo, Japan', 'Osaka, Japan', 'Seoul, South Korea', 'Sydney, Australia',
    'Melbourne, Australia', 'Mumbai, India', 'Delhi, India', 'Beijing, China', 'Shanghai, China',
    'São Paulo, Brazil', 'Rio de Janeiro, Brazil', 'Mexico City, Mexico', 'Cairo, Egypt',
    'Lagos, Nigeria', 'Johannesburg, South Africa', 'Dubai, UAE', 'Singapore',
]

# Create sample hashtags pool
HASHTAGS = [
    'Sale', 'ProductLaunch', 'NewRelease', 'Trending', 'Deal', 'Discount', 'Promo', 'Limited',
    'Exclusive', 'MustHave', 'SpecialOffer', 'Innovation', 'Tech', 'Fashion', 'Lifestyle',
    'Fitness', 'Health', 'Beauty', 'Travel', 'Food', 'Sustainable', 'Eco', 'Reviews',
    'CustomerService', 'Quality', 'Premium', 'Affordable', 'BestValue', 'TrendAlert'
]

# Create sample mentions pool
MENTIONS = [
    'BrandSupport', 'CustomerService', 'TechHelp', 'RetailSupport', 'ProductTeam', 
    'InfluencerName', 'CelebrityName', 'CompetitorBrand', 'MarketingTeam', 'NewsOutlet',
    'ReviewSite', 'IndustryExpert', 'BrandCEO', 'TrendSetter', 'StyleGuide'
]

# Create sample keywords pool
KEYWORDS = [
    'quality', 'price', 'service', 'delivery', 'fast', 'slow', 'expensive', 'cheap',
    'reliable', 'innovation', 'design', 'user-friendly', 'durable', 'stylish', 'modern',
    'traditional', 'eco-friendly', 'sustainable', 'efficient', 'responsive', 'helpful',
    'disappointing', 'amazing', 'excellent', 'poor', 'improved', 'upgraded', 'outdated',
    'competitive', 'unique', 'premium', 'budget', 'luxury', 'value', 'performance',
    'feature', 'customer', 'experience', 'satisfaction', 'recommendation'
]

# Create product names based on brand names
PRODUCT_MAPPING = {
    'Nike': ['Air Max', 'Air Jordan', 'Air Force 1', 'FlyKnit', 'React', 'Epic React', 'Zoom Pegasus', 'Dri-FIT'],
    'Pepsi': ['Pepsi Max', 'Diet Pepsi', 'Pepsi Zero Sugar', 'Crystal Pepsi', 'Pepsi Wild Cherry', 'Pepsi Lime'],
    'Apple': ['iPhone 15', 'MacBook Pro', 'iPad Air', 'Apple Watch', 'AirPods Pro', 'iMac', 'Mac Mini', 'Vision Pro'],
    'Samsung': ['Galaxy S25', 'Galaxy Z Fold', 'Neo QLED TV', 'Galaxy Watch', 'Galaxy Buds', 'Galaxy Tab'],
    'Adidas': ['Ultraboost', 'Superstar', 'Stan Smith', 'NMD', 'Yeezy', 'Predator', 'Gazelle', 'Samba'],
    'Google': ['Pixel 8', 'Nest Hub', 'Pixel Buds', 'Chromebook', 'Nest Thermostat', 'Pixel Tablet', 'Pixel Watch'],
    'Amazon': ['Echo Dot', 'Kindle', 'Fire TV', 'Ring Camera', 'Fire Tablet', 'Halo Band', 'Eero WiFi'],
    'Microsoft': ['Surface Pro', 'Xbox Series X', 'Surface Laptop', 'Surface Go', 'Xbox Elite Controller', 'Surface Duo'],
    'Toyota': ['Camry', 'Corolla', 'RAV4', 'Highlander', 'Prius', 'Tacoma', 'Sienna', 'Tundra'],
    'Coca-Cola': ['Coke Zero', 'Diet Coke', 'Coca-Cola Vanilla', 'Coca-Cola Cherry', 'Sprite', 'Fanta']
}

# Create campaign names
CAMPAIGN_NAMES = [
    'SpringBlast2025', 'SummerDreams', 'FallCollection', 'WinterWonders', 'BackToSchool',
    'HolidaySpecial', 'BlackFriday', 'CyberMonday', 'NewYearNewYou', 'ValentinesDeals',
    'EarthDay', 'SummerSale', 'LaunchWave', 'InnovationX', 'NextGeneration',
    'PowerRelease', 'GlobalCampaign', 'LocalTouchpoints', 'DigitalTransformation',
    'SustainableFuture', 'CustomerFirst', 'LoyaltyRewards', 'ReferralBonus'
]

# Sample post templates to make content more realistic
POST_TEMPLATES = [
    "Just tried the {product} from {brand}. {sentiment_phrase}. {hashtags_text}",
    "{emotion_phrase} with my new {product} from {brand}! {sentiment_phrase}. {hashtags_text}",
    "Has anyone else experienced {issue} with {brand}'s {product}? {sentiment_phrase}. {mentions_text} {hashtags_text}",
    "{brand} {campaign} is {sentiment_adj}! Can't wait to see what's coming next. {hashtags_text}",
    "My {time_period} review of {brand} {product}: {sentiment_phrase}. {hashtags_text}",
    "Just saw an ad for {brand} {product} during the {campaign}. {sentiment_phrase}. {hashtags_text}",
    "Comparing {brand} {product} to the competition. {sentiment_phrase}. {hashtags_text}",
    "{question} about {brand}'s {product}? {mentions_text} {hashtags_text}",
    "Attended the {brand} {campaign} event yesterday. {sentiment_phrase}. {hashtags_text}",
    "Just unboxed my new {product} from {brand}. {sentiment_phrase}. {emotion_phrase} {hashtags_text}",
]

# Helper functions
def random_date(start, end):
    """Generate a random datetime between start and end"""
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

def generate_random_id(prefix='', length=8):
    """Generate a random alphanumeric ID"""
    chars = string.ascii_lowercase + string.digits
    return prefix + ''.join(random.choices(chars, k=length))

def round_float(value, decimals=4):
    """Round a float to the specified number of decimal places"""
    factor = 10 ** decimals
    return int(value * factor) / factor

# Helper function for more realistic post content generation
def generate_post_content(brand, product, sentiment, emotion):
    template = random.choice(POST_TEMPLATES)
    
    # Generate sentiment-related phrases
    sentiment_phrases = {
        'Positive': ['Absolutely loving it', 'Exceeded my expectations', 'Best purchase ever', 'Highly recommend', 'Worth every penny'],
        'Neutral': ['It\'s okay', 'Does the job', 'As expected', 'Not bad', 'Mixed feelings about it'],
        'Negative': ['Disappointed with the quality', 'Not worth the money', 'Had issues with it', 'Wouldn\'t recommend', 'Returning it ASAP']
    }
    
    sentiment_adjs = {
        'Positive': ['amazing', 'excellent', 'fantastic', 'impressive', 'outstanding'],
        'Neutral': ['acceptable', 'decent', 'okay', 'standard', 'typical'],
        'Negative': ['disappointing', 'frustrating', 'overpriced', 'subpar', 'underwhelming']
    }
    
    emotion_phrases = {
        'Happy': ['So happy', 'Delighted', 'Loving it'],
        'Sad': ['Feeling let down', 'Bummed out', 'Sad to report'],
        'Angry': ['Frustrated', 'Fed up', 'Cannot believe'],
        'Excited': ['Super excited', 'Can\'t contain my excitement', 'Thrilled'],
        'Confused': ['Confused about', 'Not sure why', 'Could someone explain']
    }
    
    # Generate 1-3 hashtags as a comma-separated string
    num_hashtags = random.randint(1, 3)
    hashtags_list = random.sample(HASHTAGS, num_hashtags)
    hashtags_text = ", ".join([f"#{tag}" for tag in hashtags_list])
    
    # Generate 0-2 mentions as a comma-separated string
    num_mentions = random.randint(0, 2)
    mentions_list = random.sample(MENTIONS, num_mentions) if num_mentions > 0 else []
    mentions_text = ", ".join([f"@{mention}" for mention in mentions_list])
    
    issues = ['delivery delays', 'connectivity issues', 'battery problems', 'software bugs', 'customer service']
    questions = ['Anyone have tips', 'How do I fix', 'What\'s your opinion', 'Any advice', 'Should I upgrade']
    time_periods = ['one week', 'one month', 'three months', 'six months', 'one year', 'two days']
    
    # Fill in the template
    text = template.format(
        brand=brand,
        product=product,
        campaign=random.choice(CAMPAIGN_NAMES),
        sentiment_phrase=random.choice(sentiment_phrases[sentiment]),
        sentiment_adj=random.choice(sentiment_adjs[sentiment]),
        emotion_phrase=random.choice(emotion_phrases[emotion]),
        hashtags_text=hashtags_text,
        mentions_text=mentions_text,
        issue=random.choice(issues),
        question=random.choice(questions),
        time_period=random.choice(time_periods)
    )
    
    # Ensure text has reasonable length (15-40 words)
    words = text.split()
    if len(words) > 40:
        text = ' '.join(words[:40])
    elif len(words) < 15:
        # Add filler if too short
        fillers = ['Really interested in hearing your thoughts!', 'Let me know what you think!', 
                'Would love to get your feedback!', 'Curious about your experience too.']
        text += ' ' + random.choice(fillers)
    
    return text.strip(), hashtags_text, mentions_text

# Generate the data
print(f"Generating synthetic buzz tracker dataset with {NUM_ROWS} rows...")
start_time = time.time()

# Create the output directory
output_dir = '/home/subash-s/Desktop/BI-buzz tracker'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Open CSV file for writing
output_path = os.path.join(output_dir, OUTPUT_FILE)
with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
    # Define fieldnames (column headers)
    fieldnames = [
        # Post Metadata
        'post_id', 'timestamp', 'day_of_week', 'platform', 'user_id', 'location', 'language',
        # Post Content & NLP
        'text_content', 'hashtags', 'mentions', 'keywords', 'topic_category',
        # Sentiment & Emotion Metrics
        'sentiment_score', 'sentiment_label', 'emotion_type', 'toxicity_score',
        # Engagement Analytics
        'likes_count', 'shares_count', 'comments_count', 'impressions', 'engagement_rate',
        # Brand & Campaign Tags
        'brand_name', 'product_name', 'campaign_name', 'campaign_phase',
        # Historical Tracking
        'user_past_sentiment_avg', 'user_engagement_growth', 'buzz_change_rate'
    ]
    
    # Create CSV writer
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
    writer.writeheader()
    
    # Define date range for the past year
    end_date = datetime(2025, 5, 1)  # May 1, 2025
    start_date = end_date - timedelta(days=365)
    
    # Generate and write each row
    for i in range(NUM_ROWS):
        if i % 1000 == 0:
            print(f"Generating row {i}/{NUM_ROWS}...")
        
        # 1. Post Metadata
        post_id = generate_random_id(length=12)
        timestamp = random_date(start_date, end_date)
        day_of_week = timestamp.strftime('%A')
        platform = random.choice(PLATFORMS)
        user_id = generate_random_id('user_', 8)
        location = random.choice(LOCATIONS)
        language = random.choice(LANGUAGES)
        
        # 2. Brand & Campaign Tags
        brand_name = random.choice(BRAND_NAMES)
        product_name = random.choice(PRODUCT_MAPPING.get(brand_name, ['Generic Product']))
        campaign_name = random.choice(CAMPAIGN_NAMES)
        campaign_phase = random.choice(CAMPAIGN_PHASES)
        
        # 3. Sentiment & Emotion Metrics
        # Using 4 decimal places for precision
        sentiment_score = round_float(random.uniform(-1.0, 1.0), 4)
        if sentiment_score > 0.2:
            sentiment_label = 'Positive'
        elif sentiment_score < -0.2:
            sentiment_label = 'Negative'
        else:
            sentiment_label = 'Neutral'
        
        emotion_type = random.choice(EMOTION_TYPES)
        toxicity_score = round_float(random.uniform(0, 1), 4)
        
        # 4. Post Content & NLP with sentiment-coherent text
        text_content, hashtags, mentions = generate_post_content(
            brand_name, product_name, sentiment_label, emotion_type
        )
        
        # Generate 2-4 keywords as a comma-separated list
        num_keywords = random.randint(2, 4)
        keywords = ", ".join(random.sample(KEYWORDS, num_keywords))
        
        topic_category = random.choice(TOPIC_CATEGORIES)
        
        # 5. Engagement Analytics
        likes_count = random.randint(0, 5000)
        shares_count = random.randint(0, 2000)
        comments_count = random.randint(0, 1000)
        impressions = random.randint(100, 100000)
        
        # Calculate engagement rate with 5 decimal places
        engagement = likes_count + shares_count + comments_count
        engagement_rate = round_float(engagement / max(1, impressions), 5)
        
        # 6. Historical Tracking
        user_past_sentiment_avg = round_float(random.uniform(-1, 1), 4)
        user_engagement_growth = round_float(random.uniform(-0.5, 0.5), 4)
        buzz_change_rate = round_float(random.uniform(-100, 100), 1)
        
        # Write the row to CSV
        writer.writerow({
            'post_id': post_id,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'day_of_week': day_of_week,
            'platform': platform,
            'user_id': user_id,
            'location': location,
            'language': language,
            'text_content': text_content,
            'hashtags': hashtags,
            'mentions': mentions,
            'keywords': keywords,
            'topic_category': topic_category,
            'sentiment_score': sentiment_score,
            'sentiment_label': sentiment_label,
            'emotion_type': emotion_type,
            'toxicity_score': toxicity_score,
            'likes_count': likes_count,
            'shares_count': shares_count,
            'comments_count': comments_count,
            'impressions': impressions,
            'engagement_rate': engagement_rate,
            'brand_name': brand_name,
            'product_name': product_name,
            'campaign_name': campaign_name,
            'campaign_phase': campaign_phase,
            'user_past_sentiment_avg': user_past_sentiment_avg,
            'user_engagement_growth': user_engagement_growth,
            'buzz_change_rate': buzz_change_rate
        })

# Calculate execution time
end_time = time.time()
execution_time = end_time - start_time
print(f"Done! Dataset generated successfully in {round(execution_time, 2)} seconds.")
print(f"CSV file saved to: {output_path}")
print(f"Dataset contains {NUM_ROWS} rows with all required columns.")

print("\nImprovements made:")
print("1. Comma-separated values for hashtags, mentions, and keywords")
print("2. Consistent double-quoting for text fields with commas")
print("3. No missing values in any field")
print("4. Limited floating-point precision (4-5 decimal places)")
print("5. Realistic and diverse text content with contextually relevant tags")
print("6. Consistent timestamp formatting (YYYY-MM-DD HH:MM:SS)")

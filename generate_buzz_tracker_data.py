import random
from datetime import datetime, timedelta
import string
import csv
import os
import uuid

# Set random seed for reproducibility
random.seed(42)

# Helper function for pandas DataFrame-like functionality
class SimpleDataFrame:
    def __init__(self, data):
        self.data = data
        self.shape = (len(data.get(list(data.keys())[0], [])), len(data))
    
    def head(self, n=5):
        result = {}
        for key in self.data:
            result[key] = self.data[key][:n]
        return result
    
    def to_csv(self, file_path, index=False):
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Write header
            writer.writerow(self.data.keys())
            # Write rows
            for i in range(len(self.data[list(self.data.keys())[0]])):
                writer.writerow([self.data[key][i] for key in self.data])
                
    def to_excel(self, file_path, index=False):
        print(f"Excel export not available without pandas/openpyxl.")
        print(f"CSV file has been created instead at: {file_path.replace('.xlsx', '.csv')}")

# Define constants
NUM_ROWS = 12000
OUTPUT_FILE = 'buzz_tracker_dataset.csv'

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
    "Just tried the {product} from {brand}. {sentiment_phrase}. {hashtags}",
    "{emotion} with my new {product} from {brand}! {sentiment_phrase}. {hashtags}",
    "Has anyone else experienced {issue} with {brand}'s {product}? {sentiment_phrase}. {mentions} {hashtags}",
    "{brand} {campaign} is {sentiment_adj}! Can't wait to see what's coming next. {hashtags}",
    "My {time_period} review of {brand} {product}: {sentiment_phrase}. {hashtags}",
    "Just saw an ad for {brand} {product} during the {campaign}. {sentiment_phrase}. {hashtags}",
    "Comparing {brand} {product} to the competition. {sentiment_phrase}. {hashtags}",
    "{question} about {brand}'s {product}? {mentions} {hashtags}",
    "Attended the {brand} {campaign} event yesterday. {sentiment_phrase}. {hashtags}",
    "Just unboxed my new {product} from {brand}. {sentiment_phrase}. {emotion_phrase} {hashtags}",
    "After {time_period} of using {brand} {product}, here's my take: {sentiment_phrase}. {hashtags}",
    "{brand}'s customer service regarding my {product} issue was {sentiment_adj}. {mentions} {hashtags}",
    "The new {product} pricing from {brand} is {sentiment_adj}. Thoughts? {hashtags}",
    "Breaking: {brand} just announced {product} as part of their {campaign}. {sentiment_phrase}. {hashtags}",
    "PSA: {brand}'s {campaign} has some {sentiment_adj} deals on {product}! {hashtags}",
]

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
    
    # Generate 1-3 hashtags
    num_hashtags = random.randint(1, 3)
    hashtags_text = ' '.join(['#' + random.choice(HASHTAGS) for _ in range(num_hashtags)])
    
    # Generate 0-2 mentions
    num_mentions = random.randint(0, 2)
    mentions_text = ' '.join(['@' + random.choice(MENTIONS) for _ in range(num_mentions)])
    
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
        emotion=random.choice(emotion_phrases[emotion]),
        hashtags=hashtags_text,
        mentions=mentions_text,
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


def generate_data():
    print(f"Generating synthetic buzz tracker dataset with {NUM_ROWS} rows...")
    
    # Initialize the dataframe
    data = {}
    
    # 1. Post Metadata
    print("Generating post metadata...")
    data['post_id'] = [str(uuid.uuid4())[:12] for _ in range(NUM_ROWS)]
    
    # Generate timestamps for the past year
    end_date = datetime(2025, 5, 1)  # May 1, 2025
    start_date = end_date - timedelta(days=365)
    timestamps = [start_date + timedelta(
        days=random.randint(0, 365),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59)
    ) for _ in range(NUM_ROWS)]
    
    data['timestamp'] = timestamps
    data['day_of_week'] = [ts.strftime('%A') for ts in timestamps]
    data['platform'] = [random.choice(PLATFORMS) for _ in range(NUM_ROWS)]
    data['user_id'] = ['user_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) for _ in range(NUM_ROWS)]
    data['location'] = [random.choice(LOCATIONS) for _ in range(NUM_ROWS)]
    data['language'] = [random.choice(LANGUAGES) for _ in range(NUM_ROWS)]
    
    # 2. Brand & Campaign Tags first (needed for post content)
    print("Generating brand and campaign data...")
    data['brand_name'] = [random.choice(BRAND_NAMES) for _ in range(NUM_ROWS)]
    
    # Generate product names based on brand
    data['product_name'] = []
    for brand in data['brand_name']:
        products = PRODUCT_MAPPING.get(brand, ['Generic Product'])
        data['product_name'].append(random.choice(products))
    
    data['campaign_name'] = [random.choice(CAMPAIGN_NAMES) for _ in range(NUM_ROWS)]
    data['campaign_phase'] = [random.choice(CAMPAIGN_PHASES) for _ in range(NUM_ROWS)]
    
    # 3. Sentiment & Emotion Metrics
    print("Generating sentiment and emotion data...")
    # Generate sentiment scores first (will need for post content)
    sentiment_scores = [round(random.uniform(-1.0, 1.0), 2) for _ in range(NUM_ROWS)]
    data['sentiment_score'] = sentiment_scores
    
    # Determine sentiment labels based on score
    data['sentiment_label'] = []
    for score in sentiment_scores:
        if score > 0.2:
            data['sentiment_label'].append('Positive')
        elif score < -0.2:
            data['sentiment_label'].append('Negative')
        else:
            data['sentiment_label'].append('Neutral')
    
    data['emotion_type'] = [random.choice(EMOTION_TYPES) for _ in range(NUM_ROWS)]
    data['toxicity_score'] = [round(random.uniform(0, 1), 3) for _ in range(NUM_ROWS)]
    
    # 4. Post Content & NLP with sentiment-coherent text
    print("Generating post content...")
    post_content_data = [generate_post_content(
        data['brand_name'][i], 
        data['product_name'][i],
        data['sentiment_label'][i],
        data['emotion_type'][i]
    ) for i in range(NUM_ROWS)]
    
    data['text_content'] = [content[0] for content in post_content_data]
    data['hashtags'] = [content[1] for content in post_content_data]
    data['mentions'] = [content[2] for content in post_content_data]
    
    # Generate 2-4 keywords for each post
    data['keywords'] = []
    for i in range(NUM_ROWS):
        num_keywords = random.randint(2, 4)
        keywords = random.sample(KEYWORDS, num_keywords)
        data['keywords'].append(', '.join(keywords))
    
    data['topic_category'] = [random.choice(TOPIC_CATEGORIES) for _ in range(NUM_ROWS)]
    
    # 5. Engagement Analytics
    print("Generating engagement metrics...")
    data['likes_count'] = [random.randint(0, 5000) for _ in range(NUM_ROWS)]
    data['shares_count'] = [random.randint(0, 2000) for _ in range(NUM_ROWS)]
    data['comments_count'] = [random.randint(0, 1000) for _ in range(NUM_ROWS)]
    data['impressions'] = [random.randint(100, 100000) for _ in range(NUM_ROWS)]
    
    # Calculate engagement rate
    data['engagement_rate'] = []
    for i in range(NUM_ROWS):
        engagement = data['likes_count'][i] + data['shares_count'][i] + data['comments_count'][i]
        impressions = max(1, data['impressions'][i])  # Avoid division by zero
        data['engagement_rate'].append(round(engagement / impressions, 4))
    
    # 6. Historical Tracking
    print("Generating historical metrics...")
    data['user_past_sentiment_avg'] = [round(random.uniform(-1, 1), 2) for _ in range(NUM_ROWS)]
    data['user_engagement_growth'] = [round(random.uniform(-0.5, 0.5), 3) for _ in range(NUM_ROWS)]
    data['buzz_change_rate'] = [round(random.uniform(-100, 100), 1) for _ in range(NUM_ROWS)]
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Create output directory if it doesn't exist
    output_dir = Path('/home/subash-s/Desktop/BI-buzz tracker')
    output_dir.mkdir(exist_ok=True)
    
    # Save to CSV
    output_path = output_dir / OUTPUT_FILE
    print(f"Saving dataset to {output_path}...")
    df.to_csv(output_path, index=False)
    
    # Also save as Excel if pandas has openpyxl
    try:
        excel_path = output_dir / 'buzz_tracker_dataset.xlsx'
        print(f"Saving dataset to {excel_path}...")
        df.to_excel(excel_path, index=False)
        print(f"Excel file saved successfully to {excel_path}")
    except Exception as e:
        print(f"Could not save Excel file due to: {e}")
        print("You may need to install openpyxl: pip install openpyxl")
    
    print("Done! Dataset generated successfully.")
    print(f"CSV file saved to: {output_path}")
    print(f"Dataset shape: {df.shape}")
    
    # Show a sample of the dataset
    print("\nSample of the generated data:")
    print(df.head(5))
    
    return df

if __name__ == "__main__":
    generate_data()

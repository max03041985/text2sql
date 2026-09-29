from sqlalchemy import Column, String, BigInteger, Numeric, Boolean, Date, DateTime, REAL, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class MapBankCampaignData(Base):
    __tablename__ = "map_bank_campaign_data"
    __table_args__ = {"schema": "marketingdb"}

    # --- Identifiers & Demographics ---
    bankid = Column(BigInteger)
    bank = Column(String)
    membershipno = Column(BigInteger)
    unique_customer_id = Column(String, primary_key=True)
    firstname = Column(String)
    middlename = Column(String)
    lastname = Column(String)
    dateofbirth = Column(DateTime)
    cardtype = Column(String)
    islive = Column(Boolean)
    enrollmentdate = Column(DateTime)
    res_city = Column(String)
    res_state = Column(String)
    pin = Column(String)
    mobile_valid = Column(Integer)
    email_valid = Column(Integer)
    mobile = Column(String)
    email = Column(String)
    gender = Column(String)
    age = Column(Numeric)

    # --- Overall Transaction Metrics ---
    txn = Column(BigInteger)
    spend = Column(Numeric)
    atv = Column(Numeric)
    firsttxndate = Column(DateTime)
    lasttxndate = Column(DateTime)
    spendlastmonth = Column(Numeric)
    spendlast3month = Column(Numeric)
    spendlast6month = Column(Numeric)
    spendlast12month = Column(Numeric)
    txnlastmonth = Column(BigInteger)
    txnlast3month = Column(BigInteger)
    txnlast6month = Column(BigInteger)
    txnlast12month = Column(BigInteger)
    partnerspends = Column(Numeric)
    partnertxn = Column(BigInteger)
    partneratv = Column(Numeric)
    most_trans_city = Column(String)
    recent_city = Column(String)
    online_txn_count = Column(Integer)
    online_txn_spend = Column(Numeric)

    # --- 3-Month Category Metrics ---
    txn_3m_apparel = Column(BigInteger); amount_3m_apparel = Column(Numeric)
    txn_3m_electronics = Column(BigInteger); amount_3m_electronics = Column(Numeric)
    txn_3m_fnb = Column(BigInteger); amount_3m_fnb = Column(Numeric)
    txn_3m_health = Column(BigInteger); amount_3m_health = Column(Numeric)
    txn_3m_jewelry = Column(BigInteger); amount_3m_jewelry = Column(Numeric)
    txn_3m_lifestyle = Column(BigInteger); amount_3m_lifestyle = Column(Numeric)
    txn_3m_services = Column(BigInteger); amount_3m_services = Column(Numeric)
    txn_3m_travel = Column(BigInteger); amount_3m_travel = Column(Numeric)
    txn_3m_retail = Column(BigInteger); amount_3m_retail = Column(Numeric)
    txn_3m_online = Column(BigInteger); amount_3m_online = Column(Numeric)

    # --- Overall Category Metrics ---
    txn_apparel = Column(BigInteger); amount_apparel = Column(Numeric); avg_spend_apparel = Column(Numeric); last_txn_dtapparel = Column(Date)
    txn_electronics = Column(BigInteger); amount_electronics = Column(Numeric); avg_spend_electronics = Column(Numeric); last_txn_dtelectronics = Column(Date)
    txn_fnb = Column(BigInteger); amount_fnb = Column(Numeric); avg_spend_fnb = Column(Numeric); last_txn_dtfnb = Column(Date)
    txn_health = Column(BigInteger); amount_health = Column(Numeric); avg_spend_health = Column(Numeric); last_txn_dthealth = Column(Date)
    txn_jewelry = Column(BigInteger); amount_jewelry = Column(Numeric); avg_spend_jewelry = Column(Numeric); last_txn_dtjewelry = Column(Date)
    txn_lifestyle = Column(BigInteger); amount_lifestyle = Column(Numeric); avg_spend_lifestyle = Column(Numeric); last_txn_dtlifestyle = Column(Date)
    txn_services = Column(BigInteger); amount_services = Column(Numeric); avg_spend_services = Column(Numeric); last_txn_dtservices = Column(Date)
    txn_travel = Column(BigInteger); amount_travel = Column(Numeric); avg_spend_travel = Column(Numeric); last_txn_dttravel = Column(Date)
    txn_retail = Column(BigInteger); amount_retail = Column(Numeric); avg_spend_retail = Column(Numeric); last_txn_dtretail = Column(Date)
    txn_online = Column(BigInteger); amount_online = Column(Numeric); avg_spend_online = Column(Numeric); last_txn_dtonline = Column(Date)

    distinct_cat = Column(BigInteger)
    distinct_category_count_in_last1month = Column(BigInteger)
    distinct_last_6_month_spend_average = Column(Numeric)

    # --- Propensity & Persona Scores (REAL) ---
    airlines_score = Column(REAL); apparelaccessories_score = Column(REAL); apparelall_score = Column(REAL)
    apparelkids_score = Column(REAL); apparelmenandboys_score = Column(REAL); apparelservices_score = Column(REAL)
    apparelwomen_score = Column(REAL); beautyservices_score = Column(REAL); bus_score = Column(REAL)
    cabs_score = Column(REAL); cosmetics_score = Column(REAL); dental_score = Column(REAL)
    diagnostics_score = Column(REAL); education_score = Column(REAL); electronics_score = Column(REAL)
    entertainment_score = Column(REAL); eyecare_score = Column(REAL); fashion_score = Column(REAL)
    fnb_score = Column(REAL); footwear_score = Column(REAL); fuel_score = Column(REAL)
    gfdtg_score = Column(REAL); health_score = Column(REAL); home_score = Column(REAL)
    homeandhardware_score = Column(REAL); hospitals_score = Column(REAL); hotel_score = Column(REAL)
    jewellery_score = Column(REAL); lifestyle_score = Column(REAL); logisticsandcourier_score = Column(REAL)
    multibrandelectronics_score = Column(REAL); pharmacy_score = Column(REAL); pubs_score = Column(REAL)
    railways_score = Column(REAL); resturants_score = Column(REAL); retail_score = Column(REAL)
    retailoutlet_score = Column(REAL); roadway_score = Column(REAL); specialityclinics_score = Column(REAL)
    sports_score = Column(REAL); supermarkets_score = Column(REAL); telecommunication_score = Column(REAL)
    travel_score = Column(REAL); utilities_score = Column(REAL)
    
    # Persona Scores
    baby_product_buyers_score = Column(REAL); biryani_lovers_score = Column(REAL); cab_users_score = Column(REAL)
    car_bike_owner_score = Column(REAL); fast_food_chains_score = Column(REAL); frequent_bus_travellers_score = Column(REAL)
    frequent_flyers_score = Column(REAL); gamblers_score = Column(REAL); gamers_score = Column(REAL)
    insurance_buyers_score = Column(REAL); movie_lovers_score = Column(REAL); online_food_order_score = Column(REAL)
    online_grocery_buyers_score = Column(REAL); online_pharmacy_score = Column(REAL); ott_platforms_score = Column(REAL)
    philanthropist_score = Column(REAL); sports_person_score = Column(REAL)

    # --- 12-Month Aggregates ---
    offline_spends_last_12month = Column(Numeric); offline_txns_last_12month = Column(BigInteger)
    online_spends_last_12month = Column(Numeric); online_txns_last_12month = Column(BigInteger)
    apparel_spends_last_12month = Column(Numeric); apparel_txns_last_12month = Column(BigInteger); apparel_atv_last_12month = Column(Numeric)
    electronics_spends_last_12month = Column(Numeric); electronics_txns_last_12month = Column(BigInteger); electronics_atv_last_12month = Column(Numeric)
    fnb_spends_last_12month = Column(Numeric); fnb_txns_last_12month = Column(BigInteger); fnb_atv_last_12month = Column(Numeric)
    health_spends_last_12month = Column(Numeric); health_txns_last_12month = Column(BigInteger); health_atv_last_12month = Column(Numeric)
    jewelery_spends_last_12month = Column(Numeric); jewelery_txns_last_12month = Column(BigInteger); jewelery_atv_last_12month = Column(Numeric)
    lifestyle_spends_last_12month = Column(Numeric); lifestyle_txns_last_12month = Column(BigInteger); lifestyle_atv_last_12month = Column(Numeric)
    travel_spends_last_12month = Column(Numeric); travel_txns_last_12month = Column(BigInteger); travel_atv_last_12month = Column(Numeric)
    retail_spends_last_12month = Column(Numeric); retail_txns_last_12month = Column(BigInteger); retail_atv_last_12month = Column(Numeric)
    supermarts_spends_last_12month = Column(Numeric); supermarts_txns_last_12month = Column(BigInteger); supermarts_atv_last_12month = Column(Numeric)

    # --- Redemption Metrics ---
    redemptions = Column(BigInteger); redemption_amount = Column(Numeric); redemption_point = Column(Numeric); redemption_atv = Column(Numeric)
    billed_amount = Column(Numeric); first_redemption_date = Column(Date); last_redemption_date = Column(Date)
    redemption_last_1month = Column(BigInteger); redemption_amount_last_1month = Column(Numeric)
    redemption_last_3month = Column(BigInteger); redemption_amount_last_3month = Column(Numeric)
    redemption_last_6month = Column(BigInteger); redemption_amount_last_6month = Column(Numeric)
    redemption_last_9month = Column(BigInteger); redemption_amount_last_9month = Column(Numeric)
    redemption_last_12month = Column(BigInteger); redemption_amount_last_12month = Column(Numeric)
    
    partner_redemptions = Column(BigInteger); partner_redemption_amount = Column(Numeric)
    partner_redemptions_last_12month = Column(BigInteger); partner_redemption_amount_last_12month = Column(Numeric)
    partner_max_redemption_date = Column(Date)
    
    offline_redemptions = Column(BigInteger); offline_redemption_amount = Column(Numeric); offline_max_redemption_date = Column(Date)
    offline_redemptions_last_12month = Column(BigInteger); offline_redemption_amount_last_12month = Column(Numeric)
    
    online_redemptions = Column(BigInteger); online_redemption_amount = Column(Numeric); online_max_redemption_date = Column(Date)
    online_redemptions_last_12month = Column(BigInteger); online_redemption_amount_last_12month = Column(Numeric)
    
    distinct_redemption_module = Column(BigInteger); distinct_redemption_module_last_12month = Column(BigInteger)

    # --- Module Redemptions ---
    module_air_redemptions = Column(BigInteger); module_air_redemption_amount = Column(Numeric); module_air_max_redemption_date = Column(Date)
    module_bill_payment_redemptions = Column(BigInteger); module_bill_payment_redemption_amount = Column(Numeric); module_bill_payment_max_redemption_date = Column(Date)
    module_bus_redemptions = Column(BigInteger); module_bus_redemption_amount = Column(Numeric); module_bus_max_redemption_date = Column(Date)
    module_cashback_redemptions = Column(BigInteger); module_cashback_redemption_amount = Column(Numeric); module_cashback_max_redemption_date = Column(Date)
    module_donation_redemptions = Column(BigInteger); module_donation_redemption_amount = Column(Numeric); module_donation_max_redemption_date = Column(Date)
    module_dth_redemptions = Column(BigInteger); module_dth_redemption_amount = Column(Numeric); module_dth_max_redemption_date = Column(Date)
    module_elitepay_redemptions = Column(BigInteger); module_elitepay_redemption_amount = Column(Numeric); module_elitepay_max_redemption_date = Column(Date)
    module_giftcard_redemptions = Column(BigInteger); module_giftcard_redemption_amount = Column(Numeric); module_giftcard_max_redemption_date = Column(Date)
    module_hotel_redemptions = Column(BigInteger); module_hotel_redemption_amount = Column(Numeric); module_hotel_max_redemption_date = Column(Date)
    module_instore_redemptions = Column(BigInteger); module_instore_redemption_amount = Column(Numeric); module_instore_max_redemption_date = Column(Date)
    module_merchandise_redemptions = Column(BigInteger); module_merchandise_redemption_amount = Column(Numeric); module_merchandise_max_redemption_date = Column(Date)
    module_mobile_redemptions = Column(BigInteger); module_mobile_redemption_amount = Column(Numeric); module_mobile_max_redemption_date = Column(Date)
    module_movie_redemptions = Column(BigInteger); module_movie_redemption_amount = Column(Numeric); module_movie_max_redemption_date = Column(Date)
    module_mpoint_redemptions = Column(BigInteger); module_mpoint_redemption_amount = Column(Numeric); module_mpoint_max_redemption_date = Column(Date)
    module_music_redemptions = Column(BigInteger); module_music_redemption_amount = Column(Numeric); module_music_max_redemption_date = Column(Date)
    module_offers_redemptions = Column(BigInteger); module_offers_redemption_amount = Column(Numeric); module_offers_max_redemption_date = Column(Date)
    module_orc_redemptions = Column(BigInteger); module_orc_redemption_amount = Column(Numeric); module_orc_max_redemption_date = Column(Date)
    module_pointgateway_redemptions = Column(BigInteger); module_pointgateway_redemption_amount = Column(Numeric); module_pointgateway_max_redemption_date = Column(Date)
    module_pointtransfer_redemptions = Column(BigInteger); module_pointtransfer_redemption_amount = Column(Numeric); module_pointtransfer_max_redemption_date = Column(Date)

    # --- Dormancy & Activity Flags ---
    dnd = Column(Integer); reject_flag = Column(Integer); NRI_flag = Column(Integer)
    email_reachable = Column(Integer); mobile_reachable = Column(Integer)
    
    dormant_1_month_credit = Column(Integer); dormant_1_month_debit = Column(Integer)
    dormant_3_month_credit = Column(Integer); dormant_3_month_debit = Column(Integer)
    dormant_6_month_credit = Column(Integer); dormant_6_month_debit = Column(Integer)
    dormant_9_month_credit = Column(Integer); dormant_9_month_debit = Column(Integer)
    dormant_12_month_credit = Column(Integer); dormant_12_month_debit = Column(Integer)
    dormant_24_month_credit = Column(Integer); dormant_24_month_debit = Column(Integer)
    
    dormant_1_month_quarter_level_credit = Column(Integer); dormant_1_month_quarter_level_debit = Column(Integer)
    dormant_3_month_quarter_level_credit = Column(Integer); dormant_3_month_quarter_level_debit = Column(Integer)
    dormant_6_month_quarter_level_credit = Column(Integer); dormant_6_month_quarter_level_debit = Column(Integer)
    dormant_12_month_quarter_level_credit = Column(Integer); dormant_12_month_quarter_level_debit = Column(Integer)
    dormant_24_month_quarter_level_credit = Column(Integer); dormant_24_month_quarter_level_debit = Column(Integer)
    
    atm_active_last_1_year = Column(Integer)
    epos_credit_active_last_1_year = Column(Integer); epos_debit_active_last_1_year = Column(Integer)
    pos_credit_active_last_1_year = Column(Integer); pos_debit_active_last_1_year = Column(Integer)
    
    contactless_active_last_6_months_credit = Column(Integer); contactless_active_last_6_months_debit = Column(Integer)
    nevercontactless_credit = Column(Integer); nevercontactless_debit = Column(Integer)
    
    mastercard_flag = Column(Integer); visacard_flag = Column(Integer); rupaycard_flag = Column(Integer)
    
    current_quarter_active_credit = Column(Integer); current_quarter_active_debit = Column(Integer)
    last_quarter_active_credit = Column(Integer); last_quarter_active_debit = Column(Integer)
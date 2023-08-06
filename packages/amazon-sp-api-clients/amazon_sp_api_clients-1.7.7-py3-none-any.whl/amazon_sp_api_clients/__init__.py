from .vendor_transaction_status_v1 import VendorTransactionStatusV1Client
from .vendor_shipments_v1 import VendorShipmentsV1Client
from .vendor_orders_v1 import VendorOrdersV1Client
from .vendor_invoices_v1 import VendorInvoicesV1Client
from .vendor_direct_fulfillment_transactions_v1 import VendorDirectFulfillmentTransactionsV1Client
from .vendor_direct_fulfillment_shipping_v1 import VendorDirectFulfillmentShippingV1Client
from .vendor_direct_fulfillment_payments_v1 import VendorDirectFulfillmentPaymentsV1Client
from .vendor_direct_fulfillment_orders_v1 import VendorDirectFulfillmentOrdersV1Client
from .vendor_direct_fulfillment_inventory_v1 import VendorDirectFulfillmentInventoryV1Client
from .uploads_2020_11_01 import Uploads20201101Client
from .tokens_2021_03_01 import Tokens20210301Client
from .solicitations_v1 import SolicitationsV1Client
from .shipping_v1 import ShippingV1Client
from .shipment_invoicing_v0 import ShipmentInvoicingV0Client
from .services_v1 import ServicesV1Client
from .sellers_v1 import SellersV1Client
from .sales_v1 import SalesV1Client
from .reports_2021_06_30 import Reports20210630Client
from .reports_2020_09_04 import Reports20200904Client
from .product_type_definitions_2020_09_01 import ProductTypeDefinitions20200901Client
from .product_pricing_v0 import ProductPricingV0Client
from .product_fees_v0 import ProductFeesV0Client
from .orders_v0 import OrdersV0Client
from .notifications_v1 import NotificationsV1Client
from .messaging_v1 import MessagingV1Client
from .merchant_fulfillment_v0 import MerchantFulfillmentV0Client
from .listings_restrictions_2021_08_01 import ListingsRestrictions20210801Client
from .listings_items_2021_08_01 import ListingsItems20210801Client
from .listings_items_2020_09_01 import ListingsItems20200901Client
from .fulfillment_outbound_2020_07_01 import FulfillmentOutbound20200701Client
from .fulfillment_inbound_v0 import FulfillmentInboundV0Client
from .finances_v0 import FinancesV0Client
from .feeds_2021_06_30 import Feeds20210630Client
from .feeds_2020_09_04 import Feeds20200904Client
from .fba_small_and_light_v1 import FbaSmallAndLightV1Client
from .fba_inventory_v1 import FbaInventoryV1Client
from .fba_inbound_eligibility_v1 import FbaInboundEligibilityV1Client
from .catalog_items_v0 import CatalogItemsV0Client
from .catalog_items_2020_12_01 import CatalogItems20201201Client
from .authorization_v1 import AuthorizationV1Client
from .aplus_content_2020_11_01 import AplusContent20201101Client
from .marketplaces import MarketPlaces
from .report_types import ReportType, ReportTypeGroup

version = "1.7.7"
name = "amazon-sp-api-clients"
author = "Haoyu Pan"
author_email = "panhaoyu.china@outlook.com"
description = "Amazon selling partner api clients."
url = "https://github.com/panhaoyu/sp-api-clients"

import logging
from telegram import Update
from telegram.ext import ContextTypes
from utils import validate_ip, get_flag_emoji
from ip_lookup import get_ip_info
from keyboards import get_start_keyboard

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Processes /start request and outputs structured greeting panel."""
    user = update.effective_user
    welcome_text = (
        f"👋 *Welcome to the IP Address Toolkit Bot* (@Ipaddresstoolkitbot), {user.first_name}!\n\n"
        f"I am an enterprise-grade utility built to track visual telemetry and structural routing "
        f"parameters of any network endpoint globally.\n\n"
        f"💡 **Quick Action:** Simply send me any valid **IPv4** or **IPv6** address directly inside "
        f"this chat window (e.g., `8.8.8.8` or `2606:4700:4700::1111`) to begin extraction queries."
    )
    await update.message.reply_text(
        text=welcome_text, 
        parse_mode="Markdown", 
        reply_markup=get_start_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Outputs comprehensive configuration operation list manual."""
    help_text = (
        "📖 **IP Address Toolkit Bot Help Manual**\n\n"
        "⚡ *Usage Instructions:*\n"
        "Send an IP address directly to the bot. Do not add slashes, spaces, or extra sub-parameters.\n\n"
        "🛠️ *Available Text Hooks:*\n"
        "• `/start` — Reload internal environment settings components.\n"
        "• `/help` — Display this documentation module text screen.\n\n"
        "📊 *Returned Structural Attributes:*\n"
        "• Geographic: Country, State Region, City, ZIP, Visual Flag Representation.\n"
        "• Routing Metrics: Lat/Long Coordinates, Local System Timezone.\n"
        "• Autonomous Systems: ISP Carrier, Registered Organization, Upstream ASN ID.\n"
        "• Cyber Threat Feeds: Real-time checks for Hosting Proxies, Active Virtual Proxies (VPNs), or Tor relays."
    )
    
    if update.message:
        await update.message.reply_text(text=help_text, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(text=help_text, parse_mode="Markdown")

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Intercepts inline button clicks."""
    query = update.callback_query
    if query.data == "help_menu":
        await help_command(update, context)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Intercepts standard routing inputs, applies verification rules, and renders lookups."""
    ip_str = update.message.text.strip()
    
    if not validate_ip(ip_str):
        await update.message.reply_text(
            text="❌ *Invalid Format Identification Matrix*\n\n"
                 "The text provided does not match safe IPv4 or IPv6 parameters. Please verify format patterns.\n"
                 "• Expected IPv4 Example: `1.1.1.1`\n"
                 "• Expected IPv6 Example: `2001:4860:4860::8888`",
            parse_mode="Markdown"
        )
        return

    processing_msg = await update.message.reply_text(
        text="🔍 *Querying external provider dataset endpoints... Please hold.*", 
        parse_mode="Markdown"
    )
    
    try:
        ip_info = await get_ip_info(ip_str)
        if not ip_info:
            await processing_msg.edit_text(
                text="❌ *Data Extraction Error:* The provider returned empty datasets. This "
                     "typically indicates a restricted loopback, local network, or reserved IP mapping allocation."
            )
            return

        # Dataset mapping assignments
        country = ip_info.get("country", "Unknown Country")
        country_code = ip_info.get("countryCode", "")
        flag_icon = get_flag_emoji(country_code)
        region = ip_info.get("regionName", "Unknown Region")
        city = ip_info.get("city", "Unknown City")
        zip_code = ip_info.get("zip", "N/A")
        lat = ip_info.get("lat", 0.0)
        lon = ip_info.get("lon", 0.0)
        timezone = ip_info.get("timezone", "Unknown")
        isp = ip_info.get("isp", "Unknown Provider")
        org = ip_info.get("org", "Unknown Org")
        asn = ip_info.get("as", "Unknown Autonomous System")
        currency = ip_info.get("currency", "Unknown Currency")
        
        # Cyber Intelligence Flag evaluations
        is_mobile = "📱 Mobile Data Cellular Network" if ip_info.get("mobile") else "🌐 Standard Landline/Fiber Fixed Line"
        
        proxy_checks = []
        if ip_info.get("proxy"):
            proxy_checks.append("⚠️ VPN/Proxy/Tor node detected")
        if ip_info.get("hosting"):
            proxy_checks.append("🏢 Data Center / Hosting Infrastructure")
        
        security_status = ", ".join(proxy_checks) if proxy_checks else "✅ Clean Residential or Commercial ISP Endpoint"

        report = (
            f"🌐 **Telemetry Analysis Report**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📌 **Target IP Lookup:** `{ip_str}`\n\n"
            f"🌍 **Geographic Infrastructure**\n"
            f"• **Country:** {country} {flag_icon} (`{country_code}`)\n"
            f"• **Region/State:** {region}\n"
            f"• **City:** {city}\n"
            f"• **ZIP/Postal Code:** {zip_code}\n"
            f"• **Coordinates:** `{lat}, {lon}`\n"
            f"• **Local Currency:** {currency}\n"
            f"• **System Timezone:** {timezone}\n\n"
            f"🏢 **Network Service Provider Profile**\n"
            f"• **ISP Carrier Name:** {isp}\n"
            f"• **Corporate Entity:** {org}\n"
            f"• **System ASN Architecture:** `{asn}`\n\n"
            f"⚙️ **Cyber Threat & Connection Metadata**\n"
            f"• **Media Type:** {is_mobile}\n"
            f"• **Security Profile:** {security_status}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━"
        )
        await processing_msg.edit_text(text=report, parse_mode="Markdown")
        
    except Exception as error:
        logger.error(f"Critical execution fault processing IP: {ip_str}. Reason: {error}", exc_info=True)
        await processing_msg.edit_text(
            text="💥 *Internal System Framework Exception:* Unable to format report output at this moment."
        )

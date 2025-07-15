# main.py (หรือชื่อไฟล์บอทหลักของคุณ)

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv # เพิ่มเข้ามาเพื่อโหลด Token จากไฟล์ .env

# นำเข้าฟังก์ชัน server_on จากไฟล์ myserver.py
from myserver import server_on 

# **********************************************
# สำคัญ: เรียกใช้ server_on() ก่อนที่จะรันบอท Discord
# เพื่อให้ Web server เริ่มทำงานใน Thread แยกต่างหาก
# **********************************************
server_on()
print("Web server started in a separate thread.")

# โหลดค่าจากไฟล์ .env (สำหรับ Discord Bot Token)
load_dotenv() 

# กำหนด Intents ที่จำเป็น
intents = discord.Intents.default()
intents.message_content = True 

# สร้าง Bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# เหตุการณ์เมื่อบอทพร้อมใช้งาน
@bot.event
async def on_ready():
    print(f'เข้าสู่ระบบในชื่อ {bot.user.name} ({bot.user.id})')
    print('บอทพร้อมใช้งานแล้ว!')
    
    # ซิงค์ Slash Commands เมื่อบอทออนไลน์
    try:
        synced = await bot.tree.sync()
        print(f"ซิงค์ {len(synced)} คำสั่ง (/) สำเร็จแล้ว")
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการซิงค์คำสั่ง: {e}")
        
    print('---')

# Slash Command สำหรับการชำระเงิน
@bot.tree.command(name="payment", description="แสดงข้อมูลช่องทางการชำระเงิน")
async def payment(interaction: discord.Interaction):
    """
    เมื่อใช้คำสั่ง /payment บอทจะส่งรูปภาพช่องทางการชำระเงินในรูปแบบ Embed
    """
    image_url = "https://media.discordapp.net/attachments/947365126451916851/1363561745372942408/51d6ecdfad062bed7a1f68656996e9a1.jpg?ex=685a3295&is=6858e115&hm=63a826bc9f5a07318392ad087862882b07790db886739ad549cabca7fc9dcc54&=&format=webp&width=920&height=920"
    
    # สร้าง Embed
    embed = discord.Embed(
        title="✨ ช่องทางการชำระเงิน ✨", 
        description="👉 สแกน QR Code เพื่อชำระเงินได้เลยครับ/ค่ะ 👈",
        color=discord.Color.gold()
    )
    embed.set_image(url=image_url)
    embed.set_footer(text="ขอบคุณที่ใช้บริการครับ/ค่ะ 🙏")
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/3759/3759495.png") 

    await interaction.response.send_message(embed=embed, ephemeral=False)


server_on()  
bot.run(os.getenv('TOKEN')) 

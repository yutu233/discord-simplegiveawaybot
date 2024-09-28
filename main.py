"""
@author: yutu
date: 2024/09/28
goal: create a simple and not-limited giveaway-bot in discord for fun
"""
import discord
from discord.ext import commands # commands扩展用于创建基于命令的discord机器人, 支持通过命令调用机器人
from discord import app_commands # 用于定义和管理app命令(如/giveaway)
import asyncio # 异步框架, 可以实现非阻塞代码的执行
import random
import os
import dotenv # 用于读取.env文件中的环境变量

dotenv.load_dotenv('var.env')
TOKEN = os.getenv('TOKEN') # TOKEN是机器人的唯一标识符, 用于在API调用中验证身份
# 创建一个包含所需权限的 Intents 对象
intents = discord.Intents.default() # 指定机器人监听的事件
intents.message_content = True # 允许机器人访问消息内容

# 创建自定义的 Bot 类
class GiveawayBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # 通过命令树(commandtree)来管理机器人命令
        await self.tree.sync() # sync(): 将当前命令树的状态同步到discord API中


giveaway_bot = GiveawayBot()

# 用于存储正在进行的抽奖信息
giveaways = {}

# 创建一个自定义的 View，用于添加按钮
class GiveawayView(discord.ui.View):
    def __init__(self, message_id):
        super().__init__(timeout=None)
        self.message_id = message_id

    @discord.ui.button(label="🎉点此参与抽奖", style=discord.ButtonStyle.blurple, custom_id="join_giveaway")
    async def join_giveaway(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        参与抽奖活动
        
        Args:
            interaction (discord.Interaction): 用户的交互对象
            button (discord.ui.Button): 触发此函数的按钮对象
        
        Returns:
            None
        
        """
        giveaway = giveaways.get(self.message_id)
        if giveaway is None:
            await interaction.response.send_message("抽奖活动已结束, 无法参与", ephemeral=True)
            return

        user_id = interaction.user.id

        # 检查是否达到最大参与人数
        if giveaway["max_participants"] is not None:
            if len(giveaway["participants"]) >= giveaway["max_participants"]:
                await interaction.response.send_message("参与人数已满, 无法参与", ephemeral=True)
                return

        # 检查用户是否已经参与
        if user_id in giveaway["participants"]:
            await interaction.response.send_message("您已参与抽奖", ephemeral=True)
            return

        # 添加参与者
        giveaway["participants"].add(user_id)
        await interaction.response.send_message("成功参与抽奖!", ephemeral=True)

# 定义 /giveaway 命令
@giveaway_bot.tree.command(name="giveaway", description="开始一个抽奖活动")
@app_commands.describe(
    prize="奖品名称",
    duration="抽奖持续时间（分钟）",
    winners="中奖人数",
    max_participants="最大参与人数（默认为无限制）"
)
@app_commands.checks.has_permissions(administrator=True)
async def giveaway(interaction: discord.Interaction, prize: str, duration: float, winners: int = 1, max_participants: int = None):
    """
    开启抽奖活动
    
    Args:
        interaction (discord.Interaction): 触发抽奖的交互对象
        prize (str): 奖品名称
        duration (int): 抽奖持续时间，单位为分钟
        winners (int, optional): 中奖人数，默认为1
        max_participants (int, optional): 最大参与人数，不限制则为None，默认为None
    
    Returns:
        None
    
    """
    # 创建嵌入消息
    embed = discord.Embed(
        title="🎉 抽奖来咯! 🎉",
        description=(
            f"奖品：**{prize}**\n"
            f"中奖人数：{winners}\n"
            f"点击下方的按钮参与抽奖！\n"
            f"抽奖将在 {duration * 60} 秒后结束。\n"
            f"当前参与者: 0/{'∞' if max_participants is None else max_participants}"
        ),
        color=discord.Color.blue()
    )

    # 创建 View，并发送消息
    view = GiveawayView(interaction.id)
    await interaction.response.send_message(embed=embed, view=view)
    message = await interaction.original_response()

    # 记录抽奖信息
    giveaways[interaction.id] = {
        "prize": prize,
        "duration": duration,
        "winners": winners,
        "max_participants": max_participants,
        "participants": set(),
        "message": message,
        "channel": message.channel,
        "embed": embed,
        "view": view
    }

    async def update_message():
        """
        更新抽奖信息并编辑消息
        
        Args:
            无参数
        
        Returns:
            无返回值
        
        """
        # 如果giveaways.get(interaction.id)返回None，则退出循环
        while True:
            giveaway = giveaways.get(interaction.id)
            if giveaway is None:
                break
            current_participants = len(giveaway["participants"])
            max_participants_text = '∞' if max_participants is None else max_participants
            giveaway["embed"].description = (
                f"奖品: **{prize}**\n"
                f"中奖人数: **{winners}**\n"
                f"点击下方的按钮参与抽奖!\n"
                f"抽奖将在 **{duration * 60}** 秒后结束\n"
                f"当前参与者：{current_participants}/{max_participants_text}"
            )
            await message.edit(embed=giveaway["embed"], view=giveaway["view"])
            await asyncio.sleep(3)  # 每3秒更新一次

    giveaway_bot.loop.create_task(update_message())

    # 等待指定时间后结束抽奖
    await asyncio.sleep(duration * 60)

    # 获取参与者列表
    participants = giveaways[interaction.id]["participants"]

    if len(participants) < winners:
        winners = len(participants)

    if not participants:
        await message.channel.send("没有人参与抽奖, 抽奖已取消")
    else:
        # 随机选择赢家
        winner_ids = random.sample(list(participants), winners)
        winners_text = " ".join(f"<@{winner_id}>" for winner_id in winner_ids)
        await message.channel.send(f"🎉 恭喜 **{winners_text}** 获得了 **{prize}**! 🎉")

        # 发送私信给赢家
        for winner_id in winner_ids:
            winner = await giveaway_bot.fetch_user(winner_id)
            try:
                await winner.send(f"🎉 恭喜你于服务器 **电子魅魔** 中赢得了 **{prize}**!\n兑换码是: SQ2024")
            except discord.Forbidden:
                await message.channel.send(f"无法私信通知 <@{winner_id}>, 请联系客服哦~")

    # 删除抽奖记录
    del giveaways[interaction.id]

    # 禁用按钮
    view = giveaways[interaction.id]["view"]
    for child in view.children:
        child.disabled = True
    await message.edit(view=view)

# 处理错误事件
@giveaway.error
async def giveaway_error(interaction: discord.Interaction, error):
    """
    处理抽奖活动相关错误的函数
    
    Args:
        interaction (discord.Interaction): discord 交互对象
        error: 错误对象
    
    Returns:
        None
    
    """
    # 检查error对象是否是app_commands.errors.MissingPermissions的一个实例
    if isinstance(error, app_commands.errors.MissingPermissions):
        # 如果是, 表明用户缺少相应权限，返回用户错误信息
        await interaction.response.send_message("只有管理员才能发起抽奖活动", ephemeral=True)
    else:
        # 如果不是，发送通用错误信息
        await interaction.response.send_message("发生错误, 请稍后再试", ephemeral=True)

# 运行机器人
giveaway_bot.run(TOKEN)
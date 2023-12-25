import discord
from discord import app_commands
from discord.ext import commands
from ..logging.logging import logging
import random


class fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="trivia", description="Answer a random and awesome question")
    @app_commands.choices(
        difficulty=[
            app_commands.Choice(name="Medium", value="Medium"),
            app_commands.Choice(name="Hard", value="Hard"),
        ]
    )
    async def _trivia(
            self,
            interaction: discord.Interaction,
            difficulty: app_commands.Choice[str] = None,
    ):
        difficulty_value = difficulty.value if difficulty else 'Medium'
        await interaction.response.defer(thinking=True)
        quiz = get_question(difficulty_value, self.client.DBClient)
        print(quiz)
        view = Menu(quiz['correct_answer'])
        embed = make_embed_quiz(quiz)
        await interaction.followup.send(
            embed=embed,
            view=view
        )


class Menu(discord.ui.View):
    def __init__(self, correct: str):
        super().__init__(timeout=None)
        self.correct = correct
        # self.add_item(self.AnsButton(style=discord.ButtonStyle.blurple, label='A', custom_id='A', correct=correct))
        # self.add_item(self.AnsButton(style=discord.ButtonStyle.blurple, label='B', custom_id='B', correct=correct))
        # self.add_item(self.AnsButton(style=discord.ButtonStyle.blurple, label='C', custom_id='C', correct=correct))
        # self.add_item(self.AnsButton(style=discord.ButtonStyle.blurple, label='D', custom_id='D', correct=correct))
        for i in range(4):
            self.add_item(self.AnsButton(
                style=discord.ButtonStyle.blurple,
                label='A'+i,
                custom_id='A'+i,
                correct=correct
            ))

        # print(self.correct[0])

    async def callback(self, interaction: discord.Interaction):
        if interaction.custom_id == self.correct[0]:
            await interaction.response.send_message('Correct', ephemeral=True)
        else:
            await interaction.response.send_message('Wrong', ephemeral=True)

    # async def interaction_check(self, interaction: discord.Interaction):
    #     if interaction.user != self.view.message.author:
    #         await interaction.response.send_message("You cannot interact with this trivia.", ephemeral=True)
    #         return False
    #     return True

    class AnsButton(discord.ui.Button):
        def __init__(self, style: discord.ButtonStyle, label: str, custom_id: str, correct: str):
            super().__init__(style=style, label=label, custom_id=custom_id)
            self.correct = correct

        # async def process_answer(self, button: discord.ui.Button, interaction: discord.Interaction):
        #     print(123)
        #     await interaction.response.defer(thinking=True)
        #     if button.custom_id == self.correct:
        #         content = "Correct!"
        #     else:
        #         content = "Wrong!"
        #     await interaction.followup.send(content)


def get_question(difficulty: str, db):
    lc_quizzes = db['LC_db']['LC_quiz'].find({'difficulty': difficulty})
    lc_quizzes = list(lc_quizzes)
    index = random.randint(0, len(lc_quizzes) - 1)
    return lc_quizzes[index]


def make_embed_quiz(quiz):
    question = quiz['title']
    embed = discord.Embed(
        title="Trivia Question",
        description=question,
        color=0xffc01e if quiz['difficulty'] == 'Medium' else 0xef4743
    )
    options = quiz['options']
    # embed.add_field(name="Ans", value=options[0], inline=False)
    # embed.add_field(name="Ans", value=options[1], inline=False)
    # embed.add_field(name="Ans", value=options[2], inline=False)
    # embed.add_field(name="Ans", value=options[3], inline=False)
    for i in range(4):
        embed.add_field(name="Ans", value=options[i], inline=False)
    embed.add_field(name="Category", value=quiz.get('category'), inline=True)
    embed.add_field(name="Difficulty", value=quiz.get('difficulty'), inline=True)
    return embed


async def setup(client):
    await client.add_cog(fun(client), guilds=[discord.Object(id=1085444549125611530)])

# ...existing code...
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import time
from aiogram.filters import Command
import random


TOKEN = "YOUR_BOT_TOKEN"
bot = Bot(token=TOKEN)
dp = Dispatcher()
user_answers = {}


simvol = ['+', '-', '*', '/']
points = 64


kb_menu_reply = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Profile')],
        [KeyboardButton(text="Մաթեմատիկա")] ##KeyboardButton(text="Կենսաբանություն")],        
        ##[KeyboardButton(text="Հ. Պատմություն"), KeyboardButton(text="Քիմիա")]
        ], resize_keyboard=True)


kb_menu_Inline = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Profile", callback_data='Profile')],
        [InlineKeyboardButton(text="Մաթեմատիկա", callback_data='math')],
         ##InlineKeyboardButton(text="Կենսաբանություն", callback_data='kensab')],
        ##[InlineKeyboardButton(text="Հ. Պատմություն", callback_data='history'),
        ## InlineKeyboardButton(text="Քիմիա", callback_data='chemistry')],
        [InlineKeyboardButton(text="Կանոններ", callback_data='rules')]
        ])


kb_inline_math = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Կանոններ", callback_data='rules_math')],
        [InlineKeyboardButton(text="Հեշտ բարդություն", callback_data="easy_math"),
        InlineKeyboardButton(text="Միջին բարդություն", callback_data="medium_math")
        ],
        [InlineKeyboardButton(text="Դժվար բարդություն", callback_data="hard_math")], 
        ## InlineKeyboardButton(text="Շատ դժվար առաջադրանքներին:", callback_data="more_hard_math")],
        [InlineKeyboardButton(text="Հետ", callback_data="back_to_menu")]
    ])


kb_back = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Հետ", callback_data="back_to_menu")]
    ])
kb_back_to_math = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Հետ", callback_data="back_to_menu_math")]
    ])

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Բարև այստեղ մենք խաղաում ենք մաթեմատիկայի  վիկտորինա:\n Դե ինչ սկսենք... ", reply_markup=kb_menu_reply)
    await message.answer('Ընտրեք առարկան՝', reply_markup=kb_menu_Inline )



@dp.callback_query(F.data == 'Profile')
async def cb_profile(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(f"Ձեր միավորները՝ {points}։\nP.S. Միավորները պահպանվում են միայն ընթացիկ սեսիայի ընթացքում (Գրել <@Sargsyan314>", reply_markup=kb_back)


@dp.message(F.text == "Profile")
async def cmd_profile(message: types.Message):
    await message.answer(f"Ձեր միավորները՝ {points}։\nP.S. Միավորները պահպանվում են միայն ընթացիկ սեսիայի ընթացքում (Գրել <@Sargsyan314>)  ։", reply_markup=kb_back)


@dp.callback_query(F.data == 'back_to_menu')
async def cb_back_to_menu(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Ընտրեք առարկան՝", reply_markup=kb_menu_Inline)
    
    
@dp.callback_query(F.data == 'back_to_menu_math')
async def cb_back_to_menu_math(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Ընտիր դժվարությունը",reply_markup=kb_inline_math)

@dp.callback_query(F.data == 'rules')
async def cb_rules(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Կանոններ՝ \n 1. Յուրաքանչյուր ճիշտ պատասխան տալիսե միավորներ ըստ հացի բարդության և ընտրած առարկայի: \n" 
                                     "2. Սխալ պատասխանների համար միավորներ չեն տրվում և հանվում են միավորներ ըստ հացի բարդության և ընտրած առարկայի:։ \n"
                                     "3. Գրել միայն թվեր,ոչ տառեր կամ այլ նշաններ։ \n", reply_markup=kb_back)
@dp.callback_query(F.data == 'math')
async def cb_math(callback: types.CallbackQuery):   
    await callback.answer()
    await callback.message.answer("Դուք ընտրեցիք մաթեմատիկան: Դե ինչ տեսնեք թե ինչ եք կարողանում ", reply_markup=kb_inline_math)

@dp.callback_query(F.data == 'rules_math')
async def cb_rules_math(callback: types.CallbackQuery): 
    await callback.answer()
    await callback.message.edit_text("Մաթեմատիկայի կանոններ՝ \n 1. Յուրաքանչյուր ճիշտ պատասխան տալիս է միավորներ ըստ հացի բարդության։ \n" 
                                     "2. Սխալ պատասխանների համար միավորներ չեն տրվում և հանվում են  միավորներ։ \n"
                                     "3. Ցանկացած սխալ պատասխանի համար հանվում է 5 միավոր։ \n", reply_markup=kb_back_to_math)



def generate_expression(terms=2):
    # generate a safe expression without division and without zero issues
    nums = [random.randint(-1000, 1000) for _ in range(terms)]
    ops = [random.choice(simvol) for _ in range(terms-1)]
    parts = []
    for i, n in enumerate(nums):
        parts.append(str(n))
        if i < len(ops):
            parts.append(ops[i])
    expr = " ".join(parts)
    # evaluate safely
    try:
        value = eval(expr)
    except Exception:
        return generate_expression(terms)  # retry on unexpected error
    # keep integer results to match user input parsing
    if isinstance(value, float):
        if value.is_integer():
            value = int(value)
        else:
            # regenerate to keep integer answers
            return generate_expression(terms)
    return expr, int(value)



@dp.callback_query(F.data == 'easy_math')
async def cb_easy_math(callback: types.CallbackQuery):
    question, sum = generate_expression(terms=2)
    print(sum)
    user_answers[callback.from_user.id] = {'answer': sum, 'difficulty': 'easy'}
    await callback.message.edit_text(f"Հեշտ առաջադրանք: \n Ինչի է հավասար հետեվյալ արտահատությունը՝ {question}", reply_markup=kb_back_to_math) 
    await callback.answer()
    
    
@dp.callback_query(F.data == 'medium_math')
async def cb_medium_math(callback: types.CallbackQuery):
    question, sum = generate_expression(terms=3)
    print(sum)
    user_answers[callback.from_user.id] = {'answer': sum, 'difficulty': 'medium'}      
    await callback.message.edit_text(f"Միջին առաջադրանք: \n Ինչի է հավասար հետեվյալ արտահատությունը՝ {question}", reply_markup=kb_back_to_math)
    await callback.answer()    

    
@dp.callback_query(F.data == 'hard_math')
async def cb_more_hard_math(callback: types.CallbackQuery): 
    question, sum = generate_expression(terms=4) 
    print(sum)
    user_answers[callback.from_user.id] = {'answer': sum, 'difficulty': 'hard'}      
    await callback.message.edit_text(f"Շատ դժվար առաջադրանք: \n Ինչի է հավասար հետեվյալ արտահատությունը՝ {question}", reply_markup=kb_back_to_math)
    await callback.answer()      

                                    
@dp.message()
async def check_answer(message: types.Message):
    global points
    user_id = message.from_user.id
    if user_id in user_answers:
        correct_answer = user_answers[user_id]['answer']
        difficulty = user_answers[user_id]['difficulty']
        try:
            user_answer = int(message.text)
            if user_answer == correct_answer:
                if difficulty == 'easy':
                    point = 3
                    points += 3
                elif difficulty == 'medium':
                    point = 5
                    points += 5
                elif difficulty == 'hard':
                    point = 10
                    points += 10
                await message.answer(f"Ճիշտ պատասխան։ Դուք ստացաք {point} միավոր։", reply_markup=kb_back_to_math)
            else:
                if difficulty == 'easy':
                    point = 5
                    points -= 5
                elif difficulty == 'medium':
                    point = 4
                    points -= 4
                elif difficulty == 'hard':
                    point = 3
                    points -= 3
                await message.answer(f"Սխալ պատասխան։ Ճիշտ պատասխանն է՝ {correct_answer}. Դուք կորցրիք {point} միավոր։", reply_markup=kb_back_to_math)
        except ValueError:
            await message.answer("Խնդրում եմ գրեք միայն թվեր։", reply_markup=kb_back_to_math)
            return
        del user_answers[user_id]


async def main():
   await dp.start_polling(bot)
    
    
if __name__ == '__main__':
    asyncio.run(main())
    

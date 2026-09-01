import os
import random
from groq import Groq
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# التوكن الجديد بعد الإلغاء
TOKEN = "8766911595:AAEBr3WoIVw-v5x3NFLsEmU3InZPVXtB9Qk"

# مفتاح Groq API (مجاني)
GROQ_API_KEY = "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"

groq_client = Groq(api_key=GROQ_API_KEY)


def ask_groq(user_text: str) -> str:
    completion = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": "انت بوت تليجرام بترد بالعربية الفصحى مع القليل من الكلمات الإنجليزية بطريقة ودودة ومختصرة."},
            {"role": "user", "content": user_text}
        ]
    )
    return completion.choices[0].message.content

responses = {
    "السلام عليكم": "وعليكم السلام ورحمة الله وبركاته",
    "واه": "متلعبهاش وهراني ياواحد القسنطيني",
    "مهم": "صايي روح برب نبقاو نهدروا برك",
    "علاه": "وش دخلك",
    "وسيم": "@the_rouge_prince",
    "برب": "شلقماتك برب؟",
    "لا": "لا",
    "افا": "لااااااااااااااا",
    "هيه": "برافو هك أك قسنطيني",
    "تم": "يب",
    "شكرا": "زعما مأدب",
    "كافي": "يحيى؟",
    "ماتش؟": "علاه روح صلي",
    "عماد": "بيضة؟ لااااااااا خسارة عماد زعيم 🔥",
    "ياسمين": "مكانش مصطلح كافية للاسف معليش",
    "معز": "نيوزر"
}

house_images = {
    "ارين": "arren.jpg",
    "ستارك": "stark.jpg",
    "باراثيون": "baratheon.jpg",
    "لانيستر": "lannister.jpg",
    "تارغاريان": "targaryen.jpg"
}

flags = {
    "🇦🇪": "الإمارات", "🇶🇦": "قطر", "🇰🇼": "الكويت", "🇧🇭": "البحرين",
    "🇴🇲": "عُمان", "🇯🇴": "الأردن", "🇱🇧": "لبنان", "🇮🇶": "العراق",
    "🇸🇾": "سوريا", "🇯🇵": "اليابان", "🇨🇳": "الصين", "🇰🇷": "كوريا الجنوبية",
    "🇮🇳": "الهند", "🇮🇩": "إندونيسيا", "🇲🇾": "ماليزيا", "🇹🇭": "تايلاند",
    "🇻🇳": "فيتنام", "🇵🇭": "الفلبين", "🇵🇰": "باكستان", "🇺🇸": "الولايات المتحدة",
    "🇨🇦": "كندا", "🇧🇷": "البرازيل", "🇦🇷": "الأرجنتين", "🇲🇽": "المكسيك",
    "🇫🇷": "فرنسا", "🇩🇪": "ألمانيا", "🇮🇹": "إيطاليا", "🇪🇸": "إسبانيا",
    "🇬🇧": "المملكة المتحدة", "🇵🇹": "البرتغال", "🇳🇱": "هولندا", "🇨🇭": "سويسرا",
    "🇦🇹": "النمسا", "🇧🇪": "بلجيكا", "🇳🇴": "النرويج", "🇸🇪": "السويد",
    "🇫🇮": "فنلندا", "🇹🇷": "تركيا", "🇷🇺": "روسيا", "🇿🇦": "جنوب أفريقيا",
    "🇳🇬": "نيجيريا", "🇰🇪": "كينيا", "🇪🇹": "إثيوبيا", "🇦🇺": "أستراليا",
    "🇳🇿": "نيوزيلندا"
}

capitals = {
    "الجزائر": "الجزائر", "المغرب": "الرباط", "تونس": "تونس", "مصر": "القاهرة",
    "السعودية": "الرياض", "الإمارات": "أبوظبي", "قطر": "الدوحة", "الكويت": "الكويت",
    "البحرين": "المنامة", "عُمان": "مسقط", "الأردن": "عمّان", "لبنان": "بيروت",
    "العراق": "بغداد", "سوريا": "دمشق", "اليابان": "طوكيو", "الصين": "بكين",
    "كوريا الجنوبية": "سيول", "الهند": "نيودلهي", "إندونيسيا": "جاكرتا",
    "ماليزيا": "كوالالمبور", "تايلاند": "بانكوك", "فيتنام": "هانوي",
    "الفلبين": "مانيلا", "باكستان": "إسلام آباد", "الولايات المتحدة": "واشنطن",
    "كندا": "أوتاوا", "البرازيل": "برازيليا", "الأرجنتين": "بوينس آيرس",
    "المكسيك": "مكسيكو سيتي", "فرنسا": "باريس", "ألمانيا": "برلين",
    "إيطاليا": "روما", "إسبانيا": "مدريد", "المملكة المتحدة": "لندن",
    "البرتغال": "لشبونة", "هولندا": "أمستردام", "سويسرا": "برن",
    "النمسا": "فيينا", "النرويج": "أوسلو", "السويد": "ستوكهولم",
    "فنلندا": "هلسنكي", "تركيا": "أنقرة", "روسيا": "موسكو",
    "جنوب أفريقيا": "بريتوريا", "نيجيريا": "أبوجا", "كينيا": "نيروبي",
    "إثيوبيا": "أديس أبابا", "أستراليا": "كانبيرا", "نيوزيلندا": "ويلينغتون"
}

verses = [
    "﴿إِنَّ مَعَ الْعُسْرِ يُسْرًا﴾",
    "﴿وَقُل رَّبِّ زِدْنِي عِلْمًا﴾",
    "﴿إِنَّ اللَّهَ مَعَ الصَّابِرِينَ﴾",
    "﴿وَاللَّهُ خَيْرُ الرَّازِقِينَ﴾",
    "﴿وَبَشِّرِ الصَّابِرِينَ﴾",
    "﴿إِنَّ اللَّهَ غَفُورٌ رَّحِيمٌ﴾",
    "﴿لَا تَقْنَطُوا مِن رَّحْمَةِ اللَّهِ﴾",
    "﴿إِنَّ اللَّهَ لَا يُضِيعُ أَجْرَ الْمُحْسِنِينَ﴾",
    "﴿رَبِّ اشْرَحْ لِي صَدْرِي﴾",
    "﴿فَاذْكُرُونِي أَذْكُرْكُمْ﴾",
    "﴿وَتَوَكَّلْ عَلَى اللَّهِ ۚ وَكَفَىٰ بِاللَّهِ وَكِيلًا﴾",
    "﴿وَمَن يَتَّقِ اللَّهَ يَجْعَل لَّهُ مَخْرَجًا﴾",
    "﴿وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ﴾",
    "﴿إِنَّ اللَّهَ يُحِبُّ التَّوَّابِينَ﴾",
    "﴿وَاللَّهُ يُحِبُّ الْمُحْسِنِينَ﴾",
    "﴿وَاصْبِرْ وَمَا صَبْرُكَ إِلَّا بِاللَّهِ﴾",
    "﴿إِنَّ اللَّهَ بِكُلِّ شَيْءٍ عَلِيمٌ﴾",
    "﴿وَاللَّهُ عَلَىٰ كُلِّ شَيْءٍ قَدِيرٌ﴾",
    "﴿وَرَحْمَتِي وَسِعَتْ كُلَّ شَيْءٍ﴾",
    "﴿وَإِلَىٰ رَبِّكَ فَارْغَبْ﴾",
    "﴿رَبِّ زِدْنِي عِلْمًا﴾",
    "﴿الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ﴾",
    "﴿اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ﴾",
    "﴿إِنَّ رَبِّي قَرِيبٌ مُّجِيبٌ﴾",
    "﴿وَهُوَ مَعَكُمْ أَيْنَ مَا كُنتُمْ﴾",
    "﴿إِنَّ الْإِنسَانَ لَفِي خُسْرٍ﴾"
]

suggestions = [
    "روح تصلي",
    "استغفر ربي",
    "اتفرج got 😍",
    "وش دخلني أنا روح طبر راسك",
    "قول wassim is my daddy"
]

general_qa = {
    "عاصمة كينيا": "نيروبي",
    "عاصمة اليابان": "طوكيو",
    "عاصمة البرازيل": "برازيليا",
    "عاصمة استراليا": "كانبيرا",
    "عاصمة كندا": "أوتاوا",
    "عاصمة المغرب": "الرباط",
    "عاصمة تركيا": "أنقرة",
    "عاصمة الهند": "نيودلهي",
    "عاصمة روسيا": "موسكو",
    "عاصمة اسبانيا": "مدريد",
    "اطول نهر": "نهر النيل",
    "اعلى جبل": "جبل ايفرست",
    "اكبر محيط": "المحيط الهادي",
    "اصغر دولة": "الفاتيكان",
    "اكبر دولة": "روسيا",
    "عدد قارات العالم": "7 قارات",
    "اكبر صحراء": "الصحراء الكبرى",
    "اكبر كوكب": "المشتري",
    "اصغر كوكب": "عطارد",
    "اقرب كوكب للشمس": "عطارد",
    "عدد كواكب المجموعة الشمسية": "8 كواكب",
    "سرعة الضوء": "300 الف كم في الثانية تقريبا",
    "غاز التنفس": "الأكسجين",
    "رمز الماء الكيميائي": "H2O",
    "مكتشف الجاذبية": "إسحاق نيوتن",
    "مخترع المصباح": "توماس اديسون",
    "اسرع حيوان بري": "الفهد",
    "اكبر حيوان بري": "الفيل",
    "اكبر حيوان في العالم": "الحوت الأزرق",
    "ملك الغابة": "الأسد",
    "اطول حيوان": "الزرافة",
    "سنة اكتشاف امريكا": "1492",
    "اول رئيس امريكي": "جورج واشنطن",
    "سنة الحرب العالمية الثانية": "1939 لـ 1945",
    "عدد لاعبين فريق كرة القدم": "11 لاعب",
    "اين اقيم كاس العالم 2022": "قطر",
    "لغة البرازيل": "البرتغالية",
    "لغة المكسيك": "الاسبانية",
    "عملة اليابان": "الين",
    "عملة امريكا": "الدولار",
}


games_menu = """🎮 قائمة الألعاب المتاحة (اكتب اسم اللعبة عشان تبدأ):

🎯 تخمين الرقم
🕵️ مين أنا
🧩 ألغاز منطقية
🔤 رتب الكلمة
⚡ أسرع واحد
❌⭕ اكس اوه
🪨 حجر ورق مقص
🎲 نرد ضد البوت
🔢 خمن الرقم بالتلميحات
🧠 صح أو خطأ
🌍 خمن الدولة
🏙️ خمن العاصمة"""

celebrities = {
    "ميسي": ["لاعب كرة قدم أرجنتيني", "فاز بكأس العالم 2022", "لعب في برشلونة"],
    "رونالدو": ["لاعب كرة قدم برتغالي", "لعب في ريال مدريد", "شعاره سيوووو"],
    "اينشتاين": ["عالم فيزياء", "اكتشف النسبية", "شعره أشعث مشهور"],
    "محمد صلاح": ["لاعب كرة قدم مصري", "يلعب في ليفربول", "يلقب بالملك"],
    "نيوتن": ["عالم فيزياء ورياضيات", "اكتشف الجاذبية", "إنجليزي الجنسية"],
    "نابليون": ["قائد عسكري فرنسي", "توج نفسه إمبراطوراً", "هُزم في واترلو"],
    "ماركيز": ["ملاكم مكسيكي أسطوري", "لقبه الرمّانة الذهبية", "توفي عام 2013"],
    "ليوناردو دافنشي": ["فنان ومخترع إيطالي", "رسم الموناليزا", "عاش في عصر النهضة"],
    "غاندي": ["زعيم هندي", "قاد حركة المقاومة السلمية", "لقب بالمهاتما"],
    "أينستاين شتاين": ["اسم غريب متعمد", "ليس شخصية حقيقية", "للتشتيت فقط"],
    "شكسبير": ["كاتب مسرحي إنجليزي", "كتب هاملت وروميو وجولييت", "يعتبر أعظم كاتب في اللغة الإنجليزية"],
    "أديسون": ["مخترع أمريكي", "اخترع المصباح الكهربائي", "سجل مئات براءات الاختراع"],
}

riddles = [
    ("شيء كلما أخذت منه كبر، فما هو؟", "الحفرة"),
    ("ما هو الشيء الذي له عين ولا يرى؟", "الإبرة"),
    ("ما الشيء الذي يمشي بلا رجلين؟", "الماء"),
    ("شيء تراه في الليل ثلاث مرات، وفي النهار مرة واحدة، فما هو؟", "حرف الليل"),
    ("ما الشيء الذي كلما زاد نقص؟", "العمر"),
    ("شيء له أسنان ولا يعض، فما هو؟", "المشط"),
    ("ما هو الشيء الذي يكسر بمجرد ذكر اسمه؟", "الصمت"),
    ("شيء يطير بلا جناح ويبكي بلا عين، فما هو؟", "السحاب"),
    ("ما هو الشيء الذي إذا وضعته يقف وإذا رفعته يقع؟", "المظلة"),
    ("شيء موجود في كل بيت لكن لا يستطيع أحد رؤيته إلا مرة واحدة، فما هو؟", "الشمس عند الشروق من النافذة"),
    ("ما هو الشيء الذي يمشي ولا يتحرك؟", "الساعة"),
    ("شيء له رأس ولا عقل له، فما هو؟", "الدبوس"),
]

scramble_words = [
    "تليجرام", "برمجة", "حاسوب", "انترنت", "مدرسة", "كرة",
    "جزائر", "طائرة", "مكتبة", "هاتف", "شمس", "قمر",
    "مفتاح", "سيارة", "جامعة", "طبيب", "معلم", "كتاب"
]

true_false = [
    ("الشمس أكبر من الأرض", "صح"),
    ("القاهرة عاصمة السعودية", "خطأ"),
    ("الفيل أكبر حيوان بري", "صح"),
    ("الماء يغلي عند 50 درجة مئوية", "خطأ"),
    ("الصين أكبر دولة من حيث عدد السكان", "خطأ"),
    ("القلب يضخ الدم في جسم الإنسان", "صح"),
    ("يوجد 7 قارات في العالم", "صح"),
    ("الضوء أسرع من الصوت", "صح"),
    ("النمسا وأستراليا نفس الدولة", "خطأ"),
    ("جبل إيفرست أعلى جبل في العالم", "صح"),
    ("العنكبوت حشرة", "خطأ"),
    ("البرازيل قارة", "خطأ"),
]

country_clues = {
    "مصر": "القارة: أفريقيا | العاصمة: القاهرة | اللغة: العربية",
    "اليابان": "القارة: آسيا | العاصمة: طوكيو | اللغة: اليابانية",
    "البرازيل": "القارة: أمريكا الجنوبية | العاصمة: برازيليا | اللغة: البرتغالية",
    "فرنسا": "القارة: أوروبا | العاصمة: باريس | اللغة: الفرنسية",
    "الجزائر": "القارة: أفريقيا | العاصمة: الجزائر | اللغة: العربية",
    "كندا": "القارة: أمريكا الشمالية | العاصمة: أوتاوا | اللغة: الإنجليزية والفرنسية",
    "الهند": "القارة: آسيا | العاصمة: نيودلهي | اللغة: الهندية والإنجليزية",
    "ألمانيا": "القارة: أوروبا | العاصمة: برلين | اللغة: الألمانية",
    "تركيا": "القارة: آسيا وأوروبا | العاصمة: أنقرة | اللغة: التركية",
    "المغرب": "القارة: أفريقيا | العاصمة: الرباط | اللغة: العربية",
    "إيطاليا": "القارة: أوروبا | العاصمة: روما | اللغة: الإيطالية",
    "الأرجنتين": "القارة: أمريكا الجنوبية | العاصمة: بوينس آيرس | اللغة: الإسبانية",
}


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text in general_qa:
        await update.message.reply_text(general_qa[text])

    elif text in responses:
        await update.message.reply_text(responses[text])

    elif text in house_images:
        photo_path = house_images[text]
        with open(photo_path, "rb") as photo:
            await update.message.reply_photo(photo)

    elif text == "اية":
        await update.message.reply_text(random.choice(verses))

    elif text == "اقتراح":
        await update.message.reply_text(random.choice(suggestions))

    elif text == "اعلام":
        flag = random.choice(list(flags.keys()))
        context.user_data["flag_answer"] = flags[flag]
        await update.message.reply_text(flag)

    elif "flag_answer" in context.user_data:
        answer = context.user_data["flag_answer"]
        if text == answer:
            await update.message.reply_text("برافو ✅")
        else:
            await update.message.reply_text(f"خطأ ❌ الإجابة هي {answer}")
        del context.user_data["flag_answer"]

    elif text == "عواصم":
        country = random.choice(list(capitals.keys()))
        context.user_data["capital_answer"] = capitals[country]
        await update.message.reply_text(f"ما عاصمة {country}؟")

    elif "capital_answer" in context.user_data:
        answer = context.user_data["capital_answer"]
        if text == answer:
            await update.message.reply_text("برافو ✅")
        else:
            await update.message.reply_text(f"خطأ ❌ الإجابة هي {answer}")
        del context.user_data["capital_answer"]

    # --- قائمة الألعاب ---
    elif text == "العاب":
        await update.message.reply_text(games_menu)

    # --- بدء الألعاب ---
    elif text == "تخمين الرقم":
        secret = random.randint(1, 100)
        context.user_data["game"] = "guess_number"
        context.user_data["secret_number"] = secret
        await update.message.reply_text("اخترت رقم من 1 إلى 100، حاول تخمنه!")

    elif text == "مين أنا":
        name = random.choice(list(celebrities.keys()))
        context.user_data["game"] = "who_am_i"
        context.user_data["who_answer"] = name
        hints = "\n".join(f"- {h}" for h in celebrities[name])
        await update.message.reply_text(f"تلميحات:\n{hints}\nمين أنا؟")

    elif text == "ألغاز منطقية":
        riddle, answer = random.choice(riddles)
        context.user_data["game"] = "riddle"
        context.user_data["riddle_answer"] = answer
        await update.message.reply_text(riddle)

    elif text == "رتب الكلمة":
        word = random.choice(scramble_words)
        letters = list(word)
        random.shuffle(letters)
        context.user_data["game"] = "scramble"
        context.user_data["scramble_answer"] = word
        await update.message.reply_text("رتب الحروف: " + " ".join(letters))

    elif text == "أسرع واحد":
        context.user_data["game"] = "fastest"
        context.user_data["fastest_word"] = "🚀"
        await update.message.reply_text("أول واحد يكتب 🚀 يفوز!")

    elif text == "اكس اوه":
        context.user_data["game"] = "tictactoe"
        context.user_data["board"] = [str(i) for i in range(1, 10)]
        context.user_data["turn"] = "X"
        board = context.user_data["board"]
        await update.message.reply_text(
            f"{board[0]}|{board[1]}|{board[2]}\n{board[3]}|{board[4]}|{board[5]}\n{board[6]}|{board[7]}|{board[8]}\nدور X، اكتب رقم الخانة (1-9)"
        )

    elif text == "حجر ورق مقص":
        context.user_data["game"] = "rps"
        await update.message.reply_text("اكتب: حجر أو ورق أو مقص")

    elif text == "نرد ضد البوت":
        user_roll = random.randint(1, 6)
        bot_roll = random.randint(1, 6)
        if user_roll > bot_roll:
            result = "فزت 🎉"
        elif user_roll < bot_roll:
            result = "خسرت 😅"
        else:
            result = "تعادل 🤝"
        await update.message.reply_text(f"نردك: {user_roll} | نرد البوت: {bot_roll}\n{result}")

    elif text == "خمن الرقم بالتلميحات":
        secret = random.randint(1, 100)
        context.user_data["game"] = "guess_hint"
        context.user_data["secret_number"] = secret
        parity = "زوجي" if secret % 2 == 0 else "فردي"
        await update.message.reply_text(f"فكرت برقم بين 1 و100، الرقم {parity}. خمن!")

    elif text == "صح أو خطأ":
        statement, answer = random.choice(true_false)
        context.user_data["game"] = "true_false"
        context.user_data["tf_answer"] = answer
        await update.message.reply_text(f"{statement}\n(اكتب: صح أو خطأ)")

    elif text == "خمن الدولة":
        country = random.choice(list(country_clues.keys()))
        context.user_data["game"] = "guess_country"
        context.user_data["country_answer"] = country
        await update.message.reply_text(f"{country_clues[country]}\nما هي الدولة؟")

    elif text == "خمن العاصمة":
        country = random.choice(list(capitals.keys()))
        context.user_data["game"] = "guess_capital2"
        context.user_data["capital2_answer"] = capitals[country]
        await update.message.reply_text(f"ما عاصمة {country}؟")

    # --- التعامل مع إجابات الألعاب الجارية ---
    elif context.user_data.get("game") == "guess_number":
        secret = context.user_data.get("secret_number")
        try:
            guess = int(text)
            if guess == secret:
                await update.message.reply_text("برافو، عرفتها! 🎉")
                context.user_data.pop("game", None)
            elif guess > secret:
                await update.message.reply_text("أصغر ⬇️")
            else:
                await update.message.reply_text("أكبر ⬆️")
        except ValueError:
            await update.message.reply_text("اكتب رقم بس")

    elif context.user_data.get("game") == "who_am_i":
        answer = context.user_data.get("who_answer")
        if text == answer:
            await update.message.reply_text("برافو ✅")
        else:
            await update.message.reply_text(f"خطأ ❌ الإجابة هي {answer}")
        context.user_data.pop("game", None)

    elif context.user_data.get("game") == "riddle":
        answer = context.user_data.get("riddle_answer")
        if text == answer:
            await update.message.reply_text("برافو ✅")
        else:
            await update.message.reply_text(f"خطأ ❌ الإجابة هي {answer}")
        context.user_data.pop("game", None)

    elif context.user_data.get("game") == "scramble":
        answer = context.user_data.get("scramble_answer")
        if text == answer:
            await update.message.reply_text("برافو ✅")
        else:
            await update.message.reply_text(f"خطأ ❌ الكلمة هي {answer}")
        context.user_data.pop("game", None)

    elif context.user_data.get("game") == "fastest":
        if text == context.user_data.get("fastest_word"):
            await update.message.reply_text(f"فزت يا {update.message.from_user.first_name}! ⚡")
            context.user_data.pop("game", None)

    elif context.user_data.get("game") == "tictactoe":
        board = context.user_data["board"]
        if text.isdigit() and 1 <= int(text) <= 9 and board[int(text) - 1] not in ("X", "O"):
            idx = int(text) - 1
            turn = context.user_data["turn"]
            board[idx] = turn
            win_lines = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
            won = any(board[a] == board[b] == board[c] == turn for a, b, c in win_lines)
            if won:
                await update.message.reply_text(f"{turn} فاز! 🎉")
                context.user_data.pop("game", None)
            elif "1" not in board and "2" not in board and "3" not in board and \
                 "4" not in board and "5" not in board and "6" not in board and \
                 "7" not in board and "8" not in board and "9" not in board:
                await update.message.reply_text("تعادل 🤝")
                context.user_data.pop("game", None)
            else:
                context.user_data["turn"] = "O" if turn == "X" else "X"
                await update.message.reply_text(
                    f"{board[0]}|{board[1]}|{board[2]}\n{board[3]}|{board[4]}|{board[5]}\n{board[6]}|{board[7]}|{board[8]}\nدور {context.user_data['turn']}"
                )
        else:
            await update.message.reply_text("خانة غير صحيحة، اختر رقم فاضي من 1-9")

    elif context.user_data.get("game") == "rps":
        choices = ["حجر", "ورق", "مقص"]
        if text in choices:
            bot_choice = random.choice(choices)
            beats = {"حجر": "مقص", "ورق": "حجر", "مقص": "ورق"}
            if text == bot_choice:
                result = "تعادل 🤝"
            elif beats[text] == bot_choice:
                result = "فزت 🎉"
            else:
                result = "خسرت 😅"
            await update.message.reply_text(f"اخترت: {text} | البوت اختار: {bot_choice}\n{result}")
            context.user_data.pop("game", None)
        else:
            await update.message.reply_text("اكتب: حجر أو ورق أو مقص")

    elif context.user_data.get("game") == "guess_hint":
        secret = context.user_data.get("secret_number")
        try:
            guess = int(text)
            if guess == secret:
                await update.message.reply_text("برافو، عرفتها! 🎉")
                context.user_data.pop("game", None)
            elif abs(guess - secret) <= 5:
                await update.message.reply_text("قريب جداً 🔥")
            elif guess > secret:
                await update.message.reply_text("أصغر ⬇️")
            else:
                await update.message.reply_text("أكبر ⬆️")
        except ValueError:
            await update.message.reply_text("اكتب رقم بس")

    elif context.user_data.get("game") == "true_false":
        answer = context.user_data.get("tf_answer")
        if text == answer:
            await update.message.reply_text("برافو ✅")
        else:
            await update.message.reply_text(f"خطأ ❌ الإجابة هي {answer}")
        context.user_data.pop("game", None)

    elif context.user_data.get("game") == "guess_country":
        answer = context.user_data.get("country_answer")
        if text == answer:
            await update.message.reply_text("برافو ✅")
        else:
            await update.messa

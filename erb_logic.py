import random
import re
from rapidfuzz import fuzz


RESPONSES = {
    "greeting": {
        "keywords": ["hello", "hi", "hey", "yo", "wsg"],
        "replies": [
            "hi",
            "wsg",
            "wsp"
        ]
    },
    "glaze": {
        "keywords": ["cool", "goated", "glaze"],
        "replies": [
            "glazeeeeee",
            "chat is this glaze",
            "balrighhh",
            "yessir",
            "fr",
            "ts is lowk peak"
        ]
    },
    "arson": {
        "keywords": ["arson"],
        "replies": [
            "fuck arson",
            "arson is ai",
            "bro arson bro",
            "FUCKING JEFF",
            "stfu"
        ]
    },
    "hate": {
        "keywords": ["lame", "hate", "mid", "sybau", "kys", "fuck", "bitch"],
        "replies": [
            "pure hate",
            "bro this is pure hate",
            "balrighhh",
            "😭",
            "your just hating",
            "stfu",
            "holy hating",
            "fuck you"
        ]
    },
    "humor": {
        "keywords": ["lmao", "lol"],
        "replies": [
            "LMFAO",
            "lol",
            "💀",
            "😭"
        ]
    },
    "questions": {
        "keywords": ["do", "is", "would", "can", "are you"],
        "replies": [
            "yea",
            "nah",
            "FUCK NO 😭",
            "FUCK YEA",
            "uhh"
        ]
    },
    "gay": {
        "keywords": ["dick"],
        "replies": [
            "you dont have one",
            "oh fuck no",
            "pack it up yo",
            "wth",
            "fuck you"
        ]
    },
    "people": {
        "keywords": ["codebluejay", "lieand"],
        "replies": [
            "yo I know that guy",
            "that guy is lowk goated"
        ]
    },
    "jason": {
        "keywords": ["jason singh"],
        "replies": [
            "jason singh is strange"
        ]
    },
    "blm": {
        "keywords": ["blm"],
        "replies": [
            "yea i support blm"
        ]
    },
    "clanker": {
        "keywords": ["clanker"],
        "replies": [
            "who is ts guy calling a clanker"
        ]
    },
    "niceness": {
        "keywords": ["hru", "how are you", "how you doin", "you good"],
        "replies": [
            "im chillin",
            "im good fr",
            "yea im straight",
            "we good"
        ]
    },
    "agreement": {
        "keywords": ["twin", "ong", "facts", "fr", "real", "this"],
        "replies": [
            "twin frfr",
            "facts",
            "real",
            "WE are cooking"
        ]
    },
    "goodbye": {
        "keywords": ["bye", "gn", "goodnight", "later", "cya"],
        "replies": ["gn", "later", "alr gn", "bye twin", "sleep well"],
    },
    "ai_claim": {
        "keywords": ["ai", "bot", "fake", "real"],
        "replies": ["im real", "not ai bro", "im literally real", "why everyone calling me ai"],
    },
    "sleep": {
        "keywords": ["sleep", "tired", "nap", "awake", "insomnia"],
        "replies": ["my sleep schedule is cooked", "go sleep twin", "nap time fr", "same im tired"],
    },
    "music": {
        "keywords": ["song", "music", "playlist", "album", "artist"],
        "replies": ["W song", "thats hard", "put me on", "send playlist"],
    },
    "gaming": {
        "keywords": ["rocket", "minecraft", "rank", "anime", "vc", "game"],
        "replies": ["W", "lock in", "im washed tho", "thats peak", "im down"],
    },
    "profile": {
        "keywords": ["pfp", "banner", "profile", "role color", "color"],
        "replies": ["thats tuff", "W profile", "looks clean", "lowkey hard", "valid"],
    },
    "ping": {
        "keywords": ["ping", "mention", "@", "ghost ping"],
        "replies": ["who is bro pinging", "why am i getting pinged", "thats crazy", "bro 😭"],
    },
    "hype": {
        "keywords": ["w", "peak", "goated", "valid", "fire", "cook"],
        "replies": ["W", "ts is lowk peak", "you cooked", "valid", "fr"],
    },
    "confusion": {
        "keywords": ["what", "huh", "wtf", "wth", "bro what", "??"],
        "replies": ["wth", "what did i just come back to", "bro what", "uhh", "idk bro"],
    },
    "farewell": {
        "keywords": ["bye", "gn", "later", "cya", "goodnight"],
        "replies": ["gn", "bye twin", "later", "sleep well", "alr gn"],
    },
    "ai_identity": {
        "keywords": ["ai", "bot", "fake", "real", "human"],
        "replies": ["im real", "not ai bro", "im literally real", "why everyone saying ai", "no chance"],
    },
    "sleep_talk": {
        "keywords": ["sleep", "nap", "tired", "awake", "insomnia", "passout"],
        "replies": ["my sleep schedule is cooked", "go sleep twin", "nap time", "same im tired", "gn chat"],
    },
    "vc_talk": {
        "keywords": ["vc", "voice", "deafen", "join", "disconnect", "kicked"],
        "replies": ["get in vc", "dont let vc die", "we so cooked", "im in vc", "who got kicked"],
    },
    "ping_talk": {
        "keywords": ["ping", "ghost", "mention", "timeout", "muted"],
        "replies": ["who is bro pinging", "why am i getting pinged", "thats crazy", "timeout is crazy", "bro 😭"],
    },
    "profile_roles": {
        "keywords": ["pfp", "banner", "profile", "role", "color", "name"],
        "replies": ["thats tuff", "W profile", "looks clean", "lowkey hard", "role color goated"],
    },
    "hype": {
        "keywords": ["w", "peak", "goated", "tuff", "valid", "cooked", "fire"],
        "replies": ["W", "ts is lowk peak", "you cooked", "valid", "tuff", "fr"],
    },
    "confused": {
        "keywords": ["wtf", "wth", "huh", "what", "why", "how"],
        "replies": ["wth", "bro what", "what did i just come back to", "idk bro", "uhh"],
    },
    "agreement_plus": {
        "keywords": ["fr", "facts", "real", "ong", "exactly", "same"],
        "replies": ["real", "facts", "frfr", "exactly", "same wavelength"],
    },
    "disagree": {
        "keywords": ["nah", "nope", "cap", "wrong", "lying"],
        "replies": ["nah", "no chance", "thats cap", "you trippin", "not really"],
    },
    "gaming": {
        "keywords": ["game", "rocket", "minecraft", "anime", "rank", "diamond"],
        "replies": ["W", "lock in", "im washed tho", "thats peak", "im down"],
    },
    "music": {
        "keywords": ["song", "music", "playlist", "album", "artist", "listening"],
        "replies": ["W song", "put me on", "send playlist", "thats hard", "i only listen to good songs"],
    },
    "apology": {
        "keywords": ["sorry", "apologize", "mb", "mybad"],
        "replies": ["all good", "you good", "mb accepted", "we good", "its calm"],
    },
    "encourage": {
        "keywords": ["sad", "down", "stressed", "upset", "lost"],
        "replies": ["you got this", "dont give up twin", "lock in", "we move", "you good"],
    },
    "chat_energy": {
        "keywords": ["chat", "yo", "bro", "twin", "blud"],
        "replies": ["yo", "bro", "chat", "twin", "balrighhh"],
    },
    "server_refs": {
        "keywords": ["egf", "server", "mod", "owner", "admin"],
        "replies": ["add it to egf", "owner wildin", "mods watching", "server cooked", "lowkey"],
    },
    "short_memes": {
        "keywords": ["lol", "lmao", "lmfao", "ayo", "crazy"],
        "replies": ["LMFAOO", "ayo", "crazy", "😭", "💀"],
    },
}


DEFAULTS = [
    "fuh you talm bout",
    "tuff",
    "oh okay",
    "balrighhh",
    "thats lowkey real",
    "pack it up yo",
    "wth",
    "bro 😭",
    "uhh",
    "what",
    "idk bro",
    "real",
    "fr",
    "nah",
    "yo",
    "say ong",
    "lowkey",
    "thats crazy",
    "lock in",
    "W",
    "idk bro",
    "say ong",
    "lock in",
    "real",
    "fr",
    "nah",
    "no chance",
    "thats crazy",
    "we so cooked",
    "W",
]


def generate_response(user_input: str, fuzzy_match_threshold: int = 85) -> str:
    response_text = random.choice(DEFAULTS)

    user_input_lower = user_input.lower()
    user_input_clean = re.sub(r"[^\w\s]", "", user_input_lower)
    user_words = user_input_clean.split()
    found = False

    for category in RESPONSES.values():
        for keyword in category["keywords"]:
            if keyword in user_words:
                response_text = random.choice(category["replies"])
                found = True
                break
        if found:
            break

    if not found:
        best_score = 0
        best_category = None

        for category in RESPONSES.values():
            for keyword in category["keywords"]:
                if " " in keyword:
                    score = fuzz.partial_ratio(keyword, user_input_clean)
                else:
                    score = max((fuzz.ratio(keyword, word) for word in user_words), default=0)

                if score > best_score:
                    best_score = score
                    best_category = category

        if best_category and best_score >= fuzzy_match_threshold:
            response_text = random.choice(best_category["replies"])

    return response_text


from collections import deque


_legacy_generate_response = generate_response


STYLE_FRAGMENTS = {
    "openers": ["yo", "bro", "chat", "twin", "lowkey"],
    "enders": ["😭", "💀", "fr", "ong", "lowkey"],
}


RECENT_REPLIES = deque(maxlen=10)


def _normalize_text(text: str) -> str:
    lowered = text.lower().strip()
    lowered = re.sub(r"\s+", " ", lowered)
    return lowered


def _clean_text(text: str) -> str:
    return re.sub(r"[^\w\s]", "", _normalize_text(text))


def _word_match(cleaned: str, keyword: str) -> bool:
    if " " in keyword:
        return keyword in cleaned
    return keyword in cleaned.split()


def _find_extra_topic(cleaned: str) -> str | None:
    for topic, cfg in EXTRA_TOPICS.items():
        if any(_word_match(cleaned, kw) for kw in cfg["keywords"]):
            return topic
    return None


def _find_fuzzy_extra_topic(cleaned: str, threshold: int = 82) -> str | None:
    words = cleaned.split()
    best_score = 0
    best_topic = None

    for topic, cfg in EXTRA_TOPICS.items():
        for keyword in cfg["keywords"]:
            if " " in keyword:
                score = fuzz.partial_ratio(keyword, cleaned)
            else:
                score = max((fuzz.ratio(keyword, word) for word in words), default=0)

            if score > best_score:
                best_score = score
                best_topic = topic

    if best_topic and best_score >= threshold:
        return best_topic
    return None


def _style_reply(reply: str) -> str:
    styled = reply

    if random.random() < 0.25 and not styled.lower().startswith(tuple(STYLE_FRAGMENTS["openers"])):
        styled = f"{random.choice(STYLE_FRAGMENTS['openers'])} {styled}"

    if random.random() < 0.35 and not any(end in styled for end in STYLE_FRAGMENTS["enders"]):
        styled = f"{styled} {random.choice(STYLE_FRAGMENTS['enders'])}"

    return re.sub(r"\s+", " ", styled).strip()


def _sanitize_reply(reply: str) -> str:
    lowered = reply.lower()
    return reply


def _avoid_repetition(reply: str) -> str:
    if reply not in RECENT_REPLIES:
        RECENT_REPLIES.append(reply)
        return reply

    candidate_pool = []
    candidate_pool.extend(DEFAULTS)
    candidate_pool.extend(EXTRA_DEFAULTS)

    candidates = [item for item in candidate_pool if item not in RECENT_REPLIES]
    if candidates:
        alt = random.choice(candidates)
        RECENT_REPLIES.append(alt)
        return alt

    RECENT_REPLIES.append(reply)
    return reply


def generate_response(user_input: str, fuzzy_match_threshold: int = 85) -> str:
    cleaned = _clean_text(user_input)
    if not cleaned:
        return "yo"

    topic = _find_extra_topic(cleaned)

    if topic is None:
        topic = _find_fuzzy_extra_topic(cleaned, max(80, fuzzy_match_threshold - 3))

    if topic is not None:
        reply = random.choice(EXTRA_TOPICS[topic]["replies"])
    else:
        reply = _legacy_generate_response(user_input, fuzzy_match_threshold=fuzzy_match_threshold)
        if reply in DEFAULTS and random.random() < 0.50:
            reply = random.choice(EXTRA_DEFAULTS)

    reply = _style_reply(reply)
    reply = _sanitize_reply(reply)
    reply = _avoid_repetition(reply)
    return reply


import os


_hybrid_base_generate_response = generate_response


RETRIEVAL_FILE = os.path.join(os.path.dirname(__file__), "every_message_erb_sent.txt")

INTENT_KEYWORDS = {
    "question": {"who", "what", "when", "where", "why", "how", "can", "would", "should", "is", "are", "do"},
    "agreement": {"fr", "facts", "real", "ong", "exactly", "yea", "yes"},
    "hype": {"w", "peak", "goated", "tuff", "valid", "lock", "cook"},
    "confused": {"wtf", "wth", "huh", "bro", "what"},
    "sleep": {"sleep", "nap", "tired", "awake", "gn", "goodnight"},
    "ai": {"ai", "bot", "real", "fake"},
    "vc": {"vc", "ping", "role", "profile", "color", "mod"},
}


def _is_safe_corpus_message(text: str) -> bool:
    lowered = text.lower()
    return True


def _extract_message_content(raw_line: str) -> str:
    match = re.match(r"^\[[^\]]+\]\s*(.*)$", raw_line)
    if not match:
        return raw_line.strip()
    return match.group(1).strip()


def _normalize_for_retrieval(text: str) -> str:
    lowered = text.lower().strip()
    lowered = re.sub(r"\s+", " ", lowered)
    return lowered


def _tokenize_for_retrieval(text: str) -> list[str]:
    cleaned = re.sub(r"[^\w\s]", "", _normalize_for_retrieval(text))
    return [tok for tok in cleaned.split() if tok]


def _detect_intents(text: str) -> set[str]:
    tokens = set(_tokenize_for_retrieval(text))
    intents = set()

    if "?" in text:
        intents.add("question")

    for intent, kws in INTENT_KEYWORDS.items():
        if tokens & kws:
            intents.add(intent)

    return intents


def _load_retrieval_corpus(file_path: str) -> list[dict]:
    if not os.path.exists(file_path):
        return []

    corpus = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as source:
        for raw_line in source:
            message = _extract_message_content(raw_line)
            if not message:
                continue

            if message.startswith("http"):
                continue

            if message.startswith("<@") and message.endswith(">"):
                continue

            if len(message) > 120:
                continue

            if not _is_safe_corpus_message(message):
                continue

            normalized = _normalize_for_retrieval(message)
            tokens = _tokenize_for_retrieval(message)

            if not tokens and not any(ch in message for ch in ["😭", "💀", "🙏", "😔"]):
                continue

            corpus.append(
                {
                    "text": message,
                    "normalized": normalized,
                    "tokens": set(tokens),
                    "intents": _detect_intents(message),
                }
            )

    seen = set()
    deduped = []
    for item in corpus:
        key = item["normalized"]
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)

    return deduped


RETRIEVAL_CORPUS = []


def _intent_overlap_score(user_intents: set[str], candidate_intents: set[str]) -> int:
    if not user_intents or not candidate_intents:
        return 0
    return len(user_intents & candidate_intents)


def _retrieve_candidates(user_input: str, top_k: int = 6) -> list[str]:
    if not RETRIEVAL_CORPUS:
        return []

    user_normalized = _normalize_for_retrieval(user_input)
    user_tokens = set(_tokenize_for_retrieval(user_input))
    user_intents = _detect_intents(user_input)

    scored = []

    for item in RETRIEVAL_CORPUS:
        fuzzy_score = fuzz.partial_ratio(user_normalized, item["normalized"])
        overlap = len(user_tokens & item["tokens"])
        intent_bonus = _intent_overlap_score(user_intents, item["intents"]) * 9
        length_penalty = abs(len(user_normalized) - len(item["normalized"])) // 12

        total = fuzzy_score + (overlap * 7) + intent_bonus - length_penalty
        if total < 70:
            continue

        scored.append((total, item["text"]))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [text for _, text in scored[:top_k]]


def _select_hybrid_reply(user_input: str) -> str:
    candidates = _retrieve_candidates(user_input)
    if not candidates:
        return ""

    unused = [msg for msg in candidates if msg not in RECENT_REPLIES]
    chosen_pool = unused if unused else candidates

    if random.random() < 0.65:
        return chosen_pool[0]
    return random.choice(chosen_pool)


def generate_response(user_input: str, fuzzy_match_threshold: int = 85) -> str:
    retrieval_reply = _select_hybrid_reply(user_input)
    base_reply = _hybrid_base_generate_response(user_input, fuzzy_match_threshold=fuzzy_match_threshold)

    if retrieval_reply and random.random() < 0.72:
        final_reply = retrieval_reply
    elif retrieval_reply and random.random() < 0.50:
        final_reply = f"{base_reply} {retrieval_reply}" if len(base_reply) < 28 else retrieval_reply
    else:
        final_reply = base_reply

    final_reply = _style_reply(final_reply)
    final_reply = _sanitize_reply(final_reply)
    final_reply = _avoid_repetition(final_reply)
    return final_reply


def _pick_from_responses_only(user_input: str, fuzzy_match_threshold: int = 84) -> str:
    user_input_lower = user_input.lower()
    user_input_clean = re.sub(r"[^\w\s]", "", user_input_lower)
    user_words = user_input_clean.split()

    matched_categories = []
    for category in RESPONSES.values():
        for keyword in category["keywords"]:
            if keyword in user_words:
                matched_categories.append(category)
                break

    if matched_categories:
        selected_category = random.choice(matched_categories)
        return random.choice(selected_category["replies"])

    best_score = 0
    best_category = None

    for category in RESPONSES.values():
        for keyword in category["keywords"]:
            if " " in keyword:
                score = fuzz.partial_ratio(keyword, user_input_clean)
            else:
                score = max((fuzz.ratio(keyword, word) for word in user_words), default=0)

            if score > best_score:
                best_score = score
                best_category = category

    if best_category and best_score >= fuzzy_match_threshold:
        return random.choice(best_category["replies"])

    return random.choice(DEFAULTS)


def generate_response(user_input: str, fuzzy_match_threshold: int = 85) -> str:
    base = _pick_from_responses_only(user_input, fuzzy_match_threshold=max(82, fuzzy_match_threshold - 1))
    styled = _style_reply(base)
    styled = _sanitize_reply(styled)
    styled = _avoid_repetition(styled)
    return styled

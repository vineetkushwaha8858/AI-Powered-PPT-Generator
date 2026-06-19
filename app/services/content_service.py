import re

class FastContentGenerator:
    def __init__(self, ai_system):
        self.ai_system = ai_system
        self.default_titles = [
            "Introduction", "Key Features", "Applications", "Challenges",
            "Recent Developments", "Future Directions", "Benefits", "Current Status",
            "Impact and Results", "Summary", "Solutions", "Use Cases", "Market Trends",
            "Innovations", "Deployment", "Management"
        ]

    def generate_fast_content(self, topic, num_slides):
        slide_titles = self._select_titles(num_slides, topic)
        slides = [{"type": "title_only", "title": topic, "subtitle": f"Overview of {topic}"}]
        for i in range(1, num_slides):
            section_title = slide_titles[i]
            bullets = self._fetch_unique_bullets(topic, section_title)
            slides.append({
                "type": "bullet",
                "title": section_title,
                "bullets": bullets
            })
        return slides

    def _select_titles(self, num_slides, topic):
        titles = [f"Overview of {topic}"] + self.default_titles
        while len(titles) < num_slides:
            titles += [f"Section {len(titles)+1}"]
        return titles[:num_slides]

    def _fetch_unique_bullets(self, topic, section):
        prompt = (
            f"Generate exactly 6 unique, non-repeating, short, factual bullet points "
            f"(4-10 words max each) about '{section}' for a presentation on '{topic}'. "
            f"Do not repeat any bullet, ensure each point is clear and professional. "
            f"Format as a numbered list, no headings."
        )
        response = self.ai_system.call_llm_fast(prompt)
        bullets = []
        if response:
            for line in response.split("\n"):
                line = line.strip()
                if re.match(r"^\d+\.\s+", line) or line.startswith(("-", "•", "*")):
                    bullet = re.sub(r'^\d+\.\s*|^[-•*]\s*', '', line).strip()
                    if bullet and 3 <= len(bullet.split()) <= 14:
                        bullets.append(bullet)
        while len(bullets) < 6:
            bullets.append("Additional Professional Point")
        return bullets[:6]

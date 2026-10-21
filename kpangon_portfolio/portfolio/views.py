from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from .forms import ContactForm
from .models import Competence, Experience

# Contenu par défaut, utilisé tant que la base est vide (modifiable ensuite via /admin).
DEFAULT_EXPERIENCES = [
    {
        "ancre": "gouvernance-sanitaire", "theme": "sante", "icone": "stethoscope",
        "titre": "Gouvernance Sanitaire & Plaidoyer National",
        "role": "Président de la PNUSS (Plateforme Nationale des Utilisateurs de Services de Santé)",
        "localite": "",
        "missions": [
            ("Direction Stratégique", "Pilotage national, coordination des instances et représentation légale des usagers du système de santé béninois."),
            ("Plaidoyer Institutionnel", "Interface majeure auprès du Ministère de la Santé, des partenaires internationaux et des structures étatiques."),
            ("Amélioration du Système de Santé", "Centralisation des besoins des populations et suivi de la qualité de l'offre de soins."),
        ],
    },
    {
        "ancre": "ferme-beatitudes", "theme": "agro", "icone": "sprout",
        "titre": "Entrepreneuriat & Développement Rural",
        "role": "Promoteur / Entrepreneur — Ferme Agro-Sylvo-Pastorale « Les Béatitudes »",
        "localite": "Commune de Tori-Bossito (Bénin)",
        "missions": [
            ("Gestion d'Exploitation Intégrée", "Agriculture, élevage pastoral et sylviculture durable."),
            ("Management & Commercialisation", "Administration, encadrement des équipes sur le terrain et structuration des circuits de vente."),
        ],
    },
    {
        "ancre": "leadership-agricole", "theme": "agro", "icone": "users",
        "titre": "Leadership Institutionnel Local",
        "role": "Président de l'Union Communale des Producteurs (UCP)",
        "localite": "Tori-Bossito",
        "missions": [
            ("Représentation & Défense des intérêts", "Représentation, syndicalisation et défense des intérêts des producteurs auprès des structures régionales et nationales."),
        ],
    },
]

DEFAULT_COMPETENCES = [
    ("landmark", "Haute Gouvernance & Dialogue Social (Santé)", "Maîtrise des enjeux du système sanitaire, plaidoyers nationaux, mobilisation de la société civile."),
    ("tractor", "Management Agro-Sylvo-Pastorale", "Expertise complète en gestion d'entreprise rurale, de l'élevage à la production agricole."),
    ("network", "Leadership Institutionnel", "Direction de réseaux complexes (échelle nationale et communale)."),
]


def _experiences():
    qs = Experience.objects.prefetch_related("missions")
    if qs.exists():
        return [
            {
                "ancre": e.ancre, "theme": e.theme, "icone": e.icone, "titre": e.titre,
                "role": e.role, "localite": e.localite,
                "missions": [(m.intitule, m.description) for m in e.missions.all()],
            }
            for e in qs
        ]
    return DEFAULT_EXPERIENCES


def _competences():
    qs = Competence.objects.all()
    if qs.exists():
        return [(c.icone, c.titre, c.description) for c in qs]
    return DEFAULT_COMPETENCES


def index(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save()
            try:
                send_mail(
                    subject=f"[Site] {msg.sujet}",
                    message=f"De : {msg.nom} <{msg.email}>\n\n{msg.message}",
                    from_email=None,
                    recipient_list=[settings.CONTACT_RECIPIENT],
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(request, "Merci ! Votre message a bien été envoyé.")
            return redirect("/#contact")
    else:
        form = ContactForm()

    return render(request, "portfolio/index.html", {
        "form": form,
        "experiences": _experiences(),
        "competences": _competences(),
    })

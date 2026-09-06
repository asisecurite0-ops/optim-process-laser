import io
import urllib.parse
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Configuration de la page
st.set_page_config(page_title="Optim-Process | Simulateur Laser 3D", layout="centered")

st.title("🔬 Simulateur de Fusion Laser (L-PBF)")
st.subheader("Optimisation des paramètres de fabrication métallique")

# Sélection du matériau
materiau = st.selectbox(
    "Choisissez le matériau :",
    ["Titane TA6V (Grade 5)", "Inox 316L (Accès Limité)", "Inconel 718 (Sur demande)"]
)

if "Inox" in materiau or "Inconel" in materiau:
    st.warning("🔒 Ce matériau fait partie de la version Entreprise. Les calculs ci-dessous utilisent la base Titane TA6V à titre démonstratif.")

# Entrée des paramètres
col1, col2 = st.columns(2)

with col1:
    puissance = st.slider("Puissance Laser (Watts)", min_value=100, max_value=500, value=280, step=10)
    vitesse = st.slider("Vitesse de Balayage (mm/s)", min_value=200, max_value=2000, value=1000, step=50)

with col2:
    epaisseur = st.number_input("Épaisseur de Couche (µm)", min_value=20, max_value=100, value=40, step=5)
    faisceau = st.number_input("Diamètre du Faisceau Spot (µm)", min_value=30, max_value=150, value=70, step=5)

# Calcul VED
h = epaisseur / 1000.0
d = faisceau / 1000.0
v = vitesse
P = puissance

ved = P / (v * h * d)

st.markdown("---")
st.metric(label="Densité d'Énergie Volumique (VED)", value=f"{round(ved, 2)} J/mm³")

# Diagnostic
if ved < 50.0:
    statut_txt = "MANQUE DE FUSION"
    st.error(f"🚨 STATUT : {statut_txt}")
    st.warning("Risque de porosité. Augmentez la puissance ou réduisez la vitesse.")
elif ved > 120.0:
    statut_txt = "SURCHAUFFE (KEYHOLE)"
    st.error(f"🚨 STATUT : {statut_txt}")
    st.warning("Risque de vaporisation. Augmentez la vitesse de balayage.")
else:
    statut_txt = "FENÊTRE OPTIMALE"
    st.success(f"✅ STATUT : {statut_txt}")
    st.info("Le bain de fusion est stable. Paramètres validés.")

# Fonction PDF
def generer_pdf(mat, p, v, e, f, val_ved, diag):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "Fiche de Conformité Réglage Laser L-PBF")
    
    c.setFont("Helvetica", 12)
    c.drawString(100, 710, f"Matériau : {mat}")
    c.drawString(100, 680, f"Puissance Laser : {p} W")
    c.drawString(100, 660, f"Vitesse de Balayage : {v} mm/s")
    c.drawString(100, 640, f"Épaisseur de Couche : {e} µm")
    c.drawString(100, 620, f"Diamètre Faisceau Spot : {f} µm")
    
    c.drawString(100, 580, f"Densité d'Énergie (VED) : {round(val_ved, 2)} J/mm³")
    c.drawString(100, 560, f"Statut Validation : {diag}")
    
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(100, 500, "Document généré par Optim-Process SaaS.")
    
    c.save()
    buffer.seek(0)
    return buffer

pdf_bytes = generer_pdf(materiau, puissance, vitesse, epaisseur, faisceau, ved, statut_txt)

st.download_button(
    label="📄 Télécharger la Fiche de Conformité PDF",
    data=pdf_bytes,
    file_name="fiche_conformite_laser.pdf",
    mime="application/pdf"
)

# Section Capture de Prospects avec envoi d'Email direct
st.markdown("---")
st.subheader("📩 Demander un accès complet (Version Entreprise)")
st.write("Obtenez un accès illimité à tous les matériaux (Inconel, Aluminium, Inox) et à l'export d'algorithmes personnalisés.")

with st.form("form_contact"):
    nom = st.text_input("Nom & Prénom")
    entreprise = st.text_input("Nom de l'Entreprise / Atelier")
    email_client = st.text_input("Adresse Email Professionnelle")
    soumis = st.form_submit_button("Envoyer la demande de démo")
    
    if soumis:
        if email_client and nom:
            # Structuration du message e-mail
            sujet = urllib.parse.quote(f"Demande de Démo SaaS - {entreprise}")
            corps = urllib.parse.quote(
                f"Bonjour,\n\nJe souhaite obtenir une démonstration de la version Entreprise.\n\n"
                f"Nom : {nom}\n"
                f"Entreprise : {entreprise}\n"
                f"Email : {email_client}\n"
            )
            
            lien_email = f"mailto:asisecurite0@gmail.com?subject={sujet}&body={corps}"
            
            st.success(f"Merci {nom} ! Cliquez sur le bouton ci-dessous pour m'envoyer directement votre demande par email.")
            st.markdown(
                f'<a href="{lien_email}" target="_blank" style="display: inline-block; padding: 10px 20px; background-color: #0E1117; color: white; text-decoration: none; border-radius: 5px;">✉️ Confirmer l\'envoi à asisecurite0@gmail.com</a>', 
                unsafe_allow_html=True
            )
        else:
            st.error("Veuillez remplir au moins votre nom et votre adresse email.")
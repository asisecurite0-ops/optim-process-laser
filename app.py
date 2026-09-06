import io
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

# Section Capture de Prospects (Formulaire Direct via FormSubmit)
st.markdown("---")
st.subheader("📩 Demander un accès complet (Version Entreprise)")
st.write("Obtenez un accès illimité à tous les matériaux (Inconel, Aluminium, Inox) et à l'export d'algorithmes personnalisés.")

form_html = """
<form action="https://formsubmit.co/asisecurite0@gmail.com" method="POST" style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; font-family: sans-serif;">
    <input type="hidden" name="_captcha" value="false">
    <input type="hidden" name="_next" value="https://optim-process-laser-6mvej4zrfiw74ktjyad8g3.streamlit.app/">
    
    <div style="margin-bottom: 12px;">
        <label style="font-weight: bold; color: #333; display: block; margin-bottom: 4px;">Nom & Prénom</label>
        <input type="text" name="Nom" required style="width: 100%; padding: 8px; border-radius: 5px; border: 1px solid #ccc; box-sizing: border-box;">
    </div>
    
    <div style="margin-bottom: 12px;">
        <label style="font-weight: bold; color: #333; display: block; margin-bottom: 4px;">Nom de l'Entreprise / Atelier</label>
        <input type="text" name="Entreprise" required style="width: 100%; padding: 8px; border-radius: 5px; border: 1px solid #ccc; box-sizing: border-box;">
    </div>
    
    <div style="margin-bottom: 16px;">
        <label style="font-weight: bold; color: #333; display: block; margin-bottom: 4px;">Adresse Email Professionnelle</label>
        <input type="email" name="Email" required style="width: 100%; padding: 8px; border-radius: 5px; border: 1px solid #ccc; box-sizing: border-box;">
    </div>
    
    <button type="submit" style="background-color: #FF4B4B; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; width: 100%;">
        🚀 Envoyer la demande de démo
    </button>
</form>
"""

st.components.v1.html(form_html, height=420)
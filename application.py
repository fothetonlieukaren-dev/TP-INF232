import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# ============================================================
# CONFIGURATION DE LA PAGE
# ============================================================
st.set_page_config(
    page_title="Analyse Ventes - Intelligence Commerciale",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# STYLE CSS PERSONNALISÉ (Design unique)
# ============================================================
st.markdown("""
<style>
    /* Fond général */
    .stApp {
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
    }
    
    /* Titre principal */
    h1 {
        color: #F59E0B;
        font-family: 'Georgia', serif;
        text-align: center;
        font-size: 3rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        border-bottom: 2px solid #F59E0B;
        padding-bottom: 15px;
    }
    
    /* Sous-titres */
    h2, h3 {
        color: #FCD34D;
        font-family: 'Georgia', serif;
    }
    
    /* Texte normal */
    p, span, div {
        color: #CBD5E1;
    }
    
    /* Labels des inputs */
    .stTextInput label, .stNumberInput label, .stSelectbox label {
        color: #FCD34D !important;
        font-weight: bold;
    }
    
    /* Cases de saisie */
    .stTextInput input, .stNumberInput input {
        background-color: #334155;
        color: white;
        border: 2px solid #475569;
        border-radius: 10px;
        padding: 10px;
    }
    
    /* Boutons */
    .stButton > button {
        background: linear-gradient(135deg, #F59E0B, #D97706);
        color: #0F172A;
        font-weight: bold;
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-size: 16px;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #FCD34D, #F59E0B);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(245, 158, 11, 0.6);
    }
    
    /* Cartes */
    .css-1r6slb0 {
        background: #1E293B;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        border: 1px solid #334155;
    }
    
    /* Tableaux */
    .stDataFrame {
        background-color: #1E293B;
        border-radius: 15px;
        overflow: hidden;
    }
    
    .stDataFrame th {
        background-color: #F59E0B !important;
        color: #0F172A !important;
        font-weight: bold;
    }
    
    /* Messages */
    .stSuccess {
        background-color: #065F46;
        color: #D1FAE5;
        border-left: 5px solid #10B981;
        border-radius: 10px;
    }
    
    .stWarning {
        background-color: #78350F;
        color: #FEF3C7;
        border-left: 5px solid #F59E0B;
        border-radius: 10px;
    }
    
    .stError {
        background-color: #7F1D1D;
        color: #FEE2E2;
        border-left: 5px solid #EF4444;
        border-radius: 10px;
    }
    
    .stInfo {
        background-color: #1E3A5F;
        color: #DBEAFE;
        border-left: 5px solid #3B82F6;
        border-radius: 10px;
    }
    
    /* Métriques */
    .stMetric {
        background: linear-gradient(135deg, #1E293B, #334155);
        border-radius: 15px;
        padding: 15px;
        border: 1px solid #475569;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #0F172A;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# INITIALISATION DE LA MÉMOIRE (Session State)
# ============================================================
if "produits" not in st.session_state:
    st.session_state.produits = []

if "ventes" not in st.session_state:
    st.session_state.ventes = {}

if "stocks" not in st.session_state:
    st.session_state.stocks = {}

if "historique" not in st.session_state:
    st.session_state.historique = []

# ============================================================
# FICHIER DE SAUVEGARDE PERMANENTE
# ============================================================
FICHIER_HISTORIQUE = "historique_ventes.csv"

def charger_historique():
    if os.path.exists(FICHIER_HISTORIQUE):
        df = pd.read_csv(FICHIER_HISTORIQUE)
        return df.to_dict('records')
    return []

def sauvegarder_historique():
    if len(st.session_state.historique) > 0:
        df = pd.DataFrame(st.session_state.historique)
        df.to_csv(FICHIER_HISTORIQUE, index=False)

# Charger l'historique au démarrage
if len(st.session_state.historique) == 0:
    st.session_state.historique = charger_historique()

# ============================================================
# BANNIÈRE PRINCIPALE
# ============================================================
st.markdown("""
<div style="
    background: linear-gradient(135deg, #F59E0B, #D97706, #B45309);
    padding: 40px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 10px 30px rgba(245, 158, 11, 0.3);
">
    <h1 style="color: #0F172A; border: none; font-size: 3rem; margin: 0; text-shadow: none;">
        📊 ANALYSE VENTES PRO
    </h1>
    <p style="color: #0F172A; font-size: 1.3rem; margin-top: 10px; font-weight: bold;">
        Identifiez vos produits stars • Maximisez vos profits • Dominez votre marché
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# ONGLETS DE NAVIGATION
# ============================================================
onglet = st.radio(
    "📋 NAVIGATION",
    ["🏠 Accueil", "📦 Gérer mes produits", "💰 Saisir les ventes", "📈 Analyse & Résultats", "📜 Historique"],
    horizontal=True,
    label_visibility="collapsed"
)

# ============================================================
# ONGLET 1 : ACCUEIL
# ============================================================
if onglet == "🏠 Accueil":
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="
            background: #1E293B;
            padding: 30px;
            border-radius: 15px;
            border: 1px solid #334155;
            height: 100%;
        ">
            <h2 style="color: #FCD34D;">🎯 COMMENT ÇA MARCHE ?</h2>
            <p style="font-size: 1.1rem;">
                1️⃣ <b>Ajoutez vos produits</b> avec leur prix<br>
                2️⃣ <b>Saisissez vos ventes</b> de la semaine<br>
                3️⃣ <b>Recevez une analyse</b> détaillée<br>
                4️⃣ <b>Suivez l'évolution</b> dans l'historique
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        nb_produits = len(st.session_state.produits)
        nb_semaines = len(st.session_state.historique)
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("📦 Produits enregistrés", nb_produits)
        with col_b:
            st.metric("📅 Semaines suivies", nb_semaines)
        
        if nb_produits == 0:
            st.warning("👆 Commencez par ajouter vos produits !")
        elif len(st.session_state.ventes) == 0:
            st.info("📊 Prêt à saisir vos ventes !")
        else:
            st.success("✅ Analyse disponible dans l'onglet Résultats !")
    
    st.divider()
    
    st.markdown("""
    <div style="text-align: center; color: #94A3B8; margin-top: 30px;">
        <p style="font-size: 1.2rem;">
            💡 <b>Le saviez-vous ?</b> Les commerces qui analysent leurs ventes 
            augmentent leur chiffre d'affaires de 15% en moyenne.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# ONGLET 2 : GÉRER LES PRODUITS
# ============================================================
elif onglet == "📦 Gérer mes produits":
    
    st.markdown("<h2 style='color: #FCD34D;'>📦 AJOUTER UN PRODUIT</h2>", unsafe_allow_html=True)
    
    with st.form("form_produit", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            nom = st.text_input("🏷️ Nom du produit", placeholder="Ex: Coca-Cola 33cl")
        with col2:
            prix = st.number_input("💶 Prix de vente (€)", min_value=0.0, value=1.0, step=0.5)
        with col3:
            categorie = st.selectbox("📂 Catégorie", [
                "🥤 Boissons", "🥨 Snacks", "🍬 Confiseries", 
                "🥫 Épicerie", "🧴 Hygiène", "📦 Autre"
            ])
        
        ajouter = st.form_submit_button("✅ AJOUTER CE PRODUIT")
        
        if ajouter:
            if nom == "":
                st.error("❌ Le nom du produit est obligatoire.")
            elif nom in [p["nom"] for p in st.session_state.produits]:
                st.error("❌ Ce produit existe déjà.")
            else:
                st.session_state.produits.append({
                    "nom": nom,
                    "prix": prix,
                    "categorie": categorie
                })
                st.success(f"✅ **{nom}** ajouté avec succès !")
                st.rerun()
    
    # Afficher le catalogue
    if len(st.session_state.produits) > 0:
        st.markdown(f"<h3 style='color: #FCD34D;'>📋 VOTRE CATALOGUE ({len(st.session_state.produits)} produits)</h3>", unsafe_allow_html=True)
        
        df = pd.DataFrame(st.session_state.produits)
        st.dataframe(df, use_container_width=True)
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if st.button("🗑️ VIDER LE CATALOGUE"):
                st.session_state.produits = []
                st.session_state.ventes = {}
                st.session_state.stocks = {}
                st.rerun()
        with col_b:
            csv = df.to_csv(index=False)
            st.download_button("📥 Exporter (CSV)", data=csv, file_name="catalogue.csv", mime="text/csv")
        with col_c:
            st.metric("💰 Prix moyen", f"{df['prix'].mean():.2f} €" if len(df) > 0 else "0 €")
    else:
        st.info("📭 Aucun produit. Ajoutez votre premier produit ci-dessus.")

# ============================================================
# ONGLET 3 : SAISIR LES VENTES
# ============================================================
elif onglet == "💰 Saisir les ventes":
    
    st.markdown("<h2 style='color: #FCD34D;'>💰 SAISIE DES VENTES DE LA SEMAINE</h2>", unsafe_allow_html=True)
    
    if len(st.session_state.produits) == 0:
        st.warning("⚠️ Ajoutez d'abord des produits dans l'onglet 'Gérer mes produits'.")
    else:
        st.markdown(f"<p style='color: #94A3B8;'>📅 Semaine du {datetime.now().strftime('%d/%m/%Y')}</p>", unsafe_allow_html=True)
        
        ventes_temp = {}
        stocks_temp = {}
        
        for produit in st.session_state.produits:
            st.markdown(f"---")
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"<h4 style='color: #FCD34D;'>{produit['categorie']} • {produit['nom']} • {produit['prix']:.2f}€</h4>", unsafe_allow_html=True)
            
            with col2:
                qte = st.number_input(f"📦 Vendus", min_value=0, value=0, key=f"v_{produit['nom']}")
                ventes_temp[produit['nom']] = qte
            
            with col3:
                stock = st.number_input(f"📋 En stock", min_value=0, value=0, key=f"s_{produit['nom']}")
                stocks_temp[produit['nom']] = stock
        
        st.markdown(f"---")
        
        if st.button("💾 ENREGISTRER LES VENTES"):
            st.session_state.ventes = ventes_temp
            st.session_state.stocks = stocks_temp
            st.success("✅ Ventes enregistrées ! Passez à l'onglet 'Analyse & Résultats'.")
            st.balloons()

# ============================================================
# ONGLET 4 : ANALYSE & RÉSULTATS
# ============================================================
elif onglet == "📈 Analyse & Résultats":
    
    st.markdown("<h2 style='color: #FCD34D;'>📈 ANALYSE DES VENTES</h2>", unsafe_allow_html=True)
    
    if len(st.session_state.ventes) == 0:
        st.warning("⚠️ Saisissez d'abord vos ventes dans l'onglet 'Saisir les ventes'.")
    else:
        ventes = st.session_state.ventes
        stocks = st.session_state.stocks
        
        # ---- BLOC 1 : PRODUIT STAR ET PRODUIT FAIBLE ----
        st.markdown("<h3 style='color: #FCD34D;'>🏆 CLASSEMENT DES VENTES</h3>", unsafe_allow_html=True)
        
        qtes = {k: v for k, v in ventes.items() if v > 0}
        
        col1, col2 = st.columns(2)
        
        with col1:
            if qtes:
                star = max(qtes, key=qtes.get)
                st.success(f"🌟 **PRODUIT STAR : {star}**")
                st.metric("Quantité vendue", f"{qtes[star]} unités")
                st.info("💡 **Action :** Mettez ce produit en vitrine. Proposez une offre groupée pour amplifier les ventes.")
            else:
                st.info("Aucune vente enregistrée.")
        
        with col2:
            if len(qtes) > 1:
                faible = min(qtes, key=qtes.get)
                st.error(f"📉 **PRODUIT FAIBLE : {faible}**")
                st.metric("Quantité vendue", f"{qtes[faible]} unités")
                st.info("💡 **Action :** Vérifiez son emplacement. Testez une réduction ou remplacez-le.")
            elif len(qtes) == 1:
                st.info("Un seul produit vendu.")
        
        st.divider()
        
        # ---- BLOC 2 : ALERTES STOCK ----
        st.markdown("<h3 style='color: #FCD34D;'>⚠️ ALERTES STOCK</h3>", unsafe_allow_html=True)
        
        alerte = False
        for nom, qte_vendue in ventes.items():
            stock_restant = stocks.get(nom, 0)
            if qte_vendue > 0 and stock_restant == 0:
                st.error(f"🚨 **{nom}** : RUPTURE DE STOCK ! Commandez immédiatement.")
                alerte = True
            elif qte_vendue > 0 and stock_restant < 5:
                st.warning(f"🛒 **{nom}** : Stock faible ({stock_restant} restants). Commandez bientôt.")
                alerte = True
        
        if not alerte:
            st.success("✅ Aucun problème de stock détecté.")
        
        st.divider()
        
        # ---- BLOC 3 : CHIFFRE D'AFFAIRES ----
        st.markdown("<h3 style='color: #FCD34D;'>💶 CHIFFRE D'AFFAIRES</h3>", unsafe_allow_html=True)
        
        ca_total = 0
        for produit in st.session_state.produits:
            nom = produit["nom"]
            prix = produit["prix"]
            qte = ventes.get(nom, 0)
            ca_produit = qte * prix
            ca_total += ca_produit
            if qte > 0:
                st.write(f"**{nom}** : {qte} × {prix:.2f}€ = **{ca_produit:.2f}€**")
        
        col_metric, _ = st.columns([1, 2])
        with col_metric:
            st.metric("💰 CHIFFRE D'AFFAIRES TOTAL", f"{ca_total:.2f} €")
        
        st.divider()
        
        # ---- BLOC 4 : GRAPHIQUE ----
        st.markdown("<h3 style='color: #FCD34D;'>📊 RÉPARTITION DES VENTES</h3>", unsafe_allow_html=True)
        
        ventes_filtrees = {k: v for k, v in ventes.items() if v > 0}
        
        if ventes_filtrees:
            fig, ax = plt.subplots(figsize=(8, 8))
            fig.patch.set_facecolor('#1E293B')
            ax.set_facecolor('#1E293B')
            
            couleurs = ['#F59E0B', '#EF4444', '#10B981', '#3B82F6', '#8B5CF6', '#EC4899']
            wedges, texts, autotexts = ax.pie(
                ventes_filtrees.values(),
                labels=ventes_filtrees.keys(),
                autopct='%1.1f%%',
                colors=couleurs[:len(ventes_filtrees)],
                startangle=90,
                textprops={'color': 'white', 'fontsize': 12}
            )
            for autotext in autotexts:
                autotext.set_color('#0F172A')
                autotext.set_fontweight('bold')
            
            ax.set_title("PART DES VENTES PAR PRODUIT", color='white', fontsize=16, fontweight='bold')
            st.pyplot(fig)
        else:
            st.info("Pas assez de données pour un graphique.")
        
        st.divider()
        
        # ---- BLOC 5 : SAUVEGARDE HISTORIQUE ----
        st.markdown("<h3 style='color: #FCD34D;'>💾 SAUVEGARDE</h3>", unsafe_allow_html=True)
        
        if st.button("📥 SAUVEGARDER DANS L'HISTORIQUE"):
            nouvelle_ligne = {
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "CA_Total": round(ca_total, 2),
                "Nb_Produits_Vendus": sum(ventes.values()),
                "Produit_Star": max(qtes, key=qtes.get) if qtes else "Aucun"
            }
            for produit in st.session_state.produits:
                nouvelle_ligne[f"{produit['nom']}_Qte"] = ventes.get(produit['nom'], 0)
            
            st.session_state.historique.append(nouvelle_ligne)
            sauvegarder_historique()
            st.success("✅ Données sauvegardées dans l'historique !")

# ============================================================
# ONGLET 5 : HISTORIQUE
# ============================================================
elif onglet == "📜 Historique":
    
    st.markdown("<h2 style='color: #FCD34D;'>📜 HISTORIQUE DES VENTES</h2>", unsafe_allow_html=True)
    
    if len(st.session_state.historique) == 0:
        st.info("📭 Aucun historique. Sauvegardez des résultats depuis l'onglet 'Analyse & Résultats'.")
    else:
        df_hist = pd.DataFrame(st.session_state.historique)
        
        st.markdown(f"<p style='color: #94A3B8;'>📊 {len(df_hist)} semaines enregistrées</p>", unsafe_allow_html=True)
        st.dataframe(df_hist, use_container_width=True)
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<h3 style='color: #FCD34D;'>📈 ÉVOLUTION DU CA</h3>", unsafe_allow_html=True)
            if "CA_Total" in df_hist.columns and len(df_hist) > 1:
                st.line_chart(df_hist, x="Date", y="CA_Total")
            else:
                st.info("Ajoutez plus de semaines pour voir l'évolution.")
        
        with col2:
            st.markdown("<h3 style='color: #FCD34D;'>📊 PRODUITS STARS LES PLUS FRÉQUENTS</h3>", unsafe_allow_html=True)
            if "Produit_Star" in df_hist.columns:
                stars_count = df_hist["Produit_Star"].value_counts()
                if len(stars_count) > 0:
                    st.bar_chart(stars_count)
        
        st.divider()
        
        col_a, col_b = st.columns(2)
        with col_a:
            csv_hist = df_hist.to_csv(index=False)
            st.download_button("📥 TÉLÉCHARGER L'HISTORIQUE (CSV)", data=csv_hist, file_name="historique_complet.csv", mime="text/csv")
        with col_b:
            if st.button("🗑️ EFFACER L'HISTORIQUE"):
                st.session_state.historique = []
                if os.path.exists(FICHIER_HISTORIQUE):
                    os.remove(FICHIER_HISTORIQUE)
                st.rerun()

# ============================================================
# PIED DE PAGE
# ============================================================
st.divider()
st.markdown("""
<div style="text-align: center; color: #64748B; padding: 20px;">
    <p>📊 <b>Analyse Ventes Pro</b> • Application développée pour le TP INF232 EC2</p>
    <p>Intelligence Commerciale • Aide à la décision • Maximisation des profits</p>
</div>
""", unsafe_allow_html=True)

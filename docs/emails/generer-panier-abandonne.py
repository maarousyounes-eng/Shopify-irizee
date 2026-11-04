# -*- coding: utf-8 -*-
u"""Genere les trois e-mails de panier abandonne d'Irizee.

Les valeurs de style ne sont pas inventees : elles sont relevees sur le site en
production (snippets/irizee-tokens.liquid et les styles calcules de
irizee.com/products/la-routine).

    Fond            #FBFAF8      Encre          #1A1A1A
    Surface         #EBEBEA      Ligne          #E2E2DF
    Carte           #FFFFFF      Texte second.  #3D3D3D
    Attenue         #5C5C5C
    Rayon 16px / interne 12px / pilule 100px
    Work Sans ; titres 800 a -0.02em ; eyebrow 12px/700/0.12em majuscules
    Bouton : noir, 14px/700, tracking 1px, majuscules, 56px de haut

Usage : python3 docs/emails/generer-panier-abandonne.py
"""

import io
import os

# ---------------------------------------------------------------- palette

BG      = u"#FBFAF8"
INK     = u"#1A1A1A"
SURFACE = u"#EBEBEA"
LINE    = u"#E2E2DF"
CARD    = u"#FFFFFF"
TEXT2   = u"#3D3D3D"
MUTED   = u"#5C5C5C"

FONT = u"'Work Sans','Helvetica Neue',Helvetica,Arial,sans-serif"
LOGO = u"https://irizee.com/cdn/shop/t/9/assets/irizee-logo.png"

# ---------------------------------------------------------------- gabarit

GABARIT = u"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="x-apple-disable-message-reformatting" />
<title>{titre}</title>
<link href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@400;600;700;800&amp;display=swap" rel="stylesheet" type="text/css" />
<style type="text/css">
  body {{ margin:0; padding:0; background-color:{bg}; -webkit-font-smoothing:antialiased; }}
  img {{ border:0; outline:none; text-decoration:none; display:block; -ms-interpolation-mode:bicubic; }}
  table {{ border-collapse:collapse; mso-table-lspace:0; mso-table-rspace:0; }}
  a {{ color:{ink}; }}
  .titre {{ font-size:44px; line-height:1.05; letter-spacing:-0.88px; }}
  @media only screen and (max-width:620px) {{
    .enveloppe {{ width:100% !important; }}
    .carte {{ border-radius:0 !important; }}
    .pad {{ padding-left:24px !important; padding-right:24px !important; }}
    .titre {{ font-size:30px !important; line-height:1.08 !important; letter-spacing:-0.6px !important; }}
    .cta {{ display:block !important; width:auto !important; }}
    .vignette {{ width:64px !important; height:64px !important; }}
    .rea td {{ display:block !important; width:100% !important; text-align:center !important; padding:5px 0 !important; }}
    .rea-sep {{ display:none !important; }}
  }}
</style>
</head>
<body style="margin:0; padding:0; background-color:{bg};">

<div style="display:none; font-size:1px; color:{bg}; line-height:1px; max-height:0; max-width:0; opacity:0; overflow:hidden;">{apercu}&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</div>

<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:{bg};">
  <tr>
    <td align="center" style="padding:36px 10px 48px;">

      <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600" class="enveloppe" style="width:600px; max-width:600px;">

        <!-- ================= logo ================= -->
        <tr>
          <td align="center" style="padding:0 0 30px;">
            <a href="https://irizee.com" style="text-decoration:none;"><img src="{logo}" width="118" height="38" alt="Irizee" style="width:118px; height:38px;" /></a>
          </td>
        </tr>

        <!-- ================= carte ================= -->
        <tr>
          <td class="carte" style="background-color:{card}; border-radius:16px;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">

              <!-- eyebrow + titre + texte -->
              <tr>
                <td class="pad" style="padding:44px 44px 0; font-family:{font};">
                  <p style="margin:0 0 14px; font-size:12px; font-weight:700; letter-spacing:1.44px; text-transform:uppercase; color:{muted};">{eyebrow}</p>
                  <h1 class="titre" style="margin:0 0 22px; font-weight:800; color:{ink};">{titre}</h1>
                  {corps}
                </td>
              </tr>

              <!-- articles du panier -->
              <tr>
                <td class="pad" style="padding:26px 44px 0;">
                  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:{surface}; border-radius:12px;">
                    <tr>
                      <td style="padding:10px 16px;">
                        {{% for item in event.extra.line_items %}}
                        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                          <tr>
                            <td width="80" valign="middle" style="padding:14px 16px 14px 0;">
                              <img class="vignette" src="{{{{ item.product.images.0.src }}}}" width="80" height="80" alt="" style="width:80px; height:80px; border-radius:8px; background-color:{card};" />
                            </td>
                            <td valign="middle" style="padding:14px 0; font-family:{font};">
                              <div style="font-size:15px; line-height:1.3; font-weight:700; color:{ink};">{{{{ item.product.title }}}}</div>
                              <div style="font-size:13px; line-height:1.5; color:{muted}; padding-top:3px;">Quantit&eacute;&nbsp;: {{{{ item.quantity|floatformat:0 }}}}</div>
                            </td>
                            <td valign="middle" align="right" style="padding:14px 0; font-family:{font}; font-size:15px; font-weight:700; color:{ink}; white-space:nowrap;">
                              {{{{ item.line_price|floatformat:2 }}}}&nbsp;&euro;
                            </td>
                          </tr>
                        </table>
                        {{% endfor %}}
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>

              <!-- bouton -->
              <tr>
                <td class="pad" style="padding:30px 44px 0;">
                  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                    <tr>
                      <td align="center" bgcolor="{ink}" style="border-radius:100px;">
                        <a class="cta" href="{{{{ event.extra.checkout_url }}}}" style="display:block; padding:19px 28px; font-family:{font}; font-size:14px; line-height:18px; font-weight:700; letter-spacing:1px; text-transform:uppercase; color:{bg}; text-decoration:none; border-radius:100px;">{bouton}</a>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>

              <!-- reassurance -->
              <tr>
                <td class="pad" style="padding:26px 44px 0;">
                  <table role="presentation" class="rea" width="100%" cellpadding="0" cellspacing="0" border="0" style="font-family:{font}; font-size:11px; font-weight:700; letter-spacing:0.9px; text-transform:uppercase; color:{muted};">
                    <tr>
                      <td align="center" style="padding:0;">Livraison offerte d&egrave;s 39&nbsp;&euro;</td>
                      <td class="rea-sep" width="28" align="center" style="color:{line};">&bull;</td>
                      <td align="center" style="padding:0;">Paiement en 4 fois</td>
                      <td class="rea-sep" width="28" align="center" style="color:{line};">&bull;</td>
                      <td align="center" style="padding:0;">Retours sous 14 jours</td>
                    </tr>
                  </table>
                </td>
              </tr>

              <!-- signature -->
              <tr>
                <td class="pad" style="padding:30px 44px 44px;">
                  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                    <tr><td style="border-top:1px solid {line}; font-size:0; line-height:0;">&nbsp;</td></tr>
                  </table>
                  <p style="margin:26px 0 0; font-family:{font}; font-size:16px; line-height:1.55; color:{text2};">{question}</p>
                  <p style="margin:16px 0 0; font-family:{font}; font-size:16px; line-height:1.55; color:{ink}; font-weight:600;">&Agrave; bient&ocirc;t,<br />Iriz&eacute;e</p>
                </td>
              </tr>

            </table>
          </td>
        </tr>

        <!-- ================= pied ================= -->
        <tr>
          <td align="center" style="padding:26px 24px 0; font-family:{font}; font-size:12px; line-height:1.75; color:{muted};">
            Vous recevez cet e-mail parce que vous avez commenc&eacute; une commande sur irizee.com.<br />
            <a href="{{% unsubscribe %}}" style="color:{muted}; text-decoration:underline;">Se d&eacute;sabonner</a><br />
            {{{{ organization.name }}}} &middot; {{{{ organization.full_address }}}}
          </td>
        </tr>

      </table>

    </td>
  </tr>
</table>
</body>
</html>
"""

P = u'<p style="margin:0 0 14px; font-family:{font}; font-size:16px; line-height:1.55; color:{text2};">{{}}</p>'.format(font=FONT, text2=TEXT2)

# ---------------------------------------------------------------- contenus

EMAILS = [
    dict(
        f=u"panier-abandonne-1.html",
        eyebrow=u"Votre panier",
        titre=u"Votre panier vous attend",
        apercu=u"Rien n’est perdu, vous pouvez reprendre où vous en étiez.",
        corps=u"".join([
            P.format(u"Bonjour,"),
            P.format(u"Vous avez commencé une commande sur irizee.com sans la terminer. "
                     u"Votre panier est toujours là, rien n’est perdu."),
        ]),
        bouton=u"Reprendre ma commande",
        question=u"Une question avant de commander ? Répondez à cet e-mail, nous lisons tout.",
    ),
    dict(
        f=u"panier-abandonne-2.html",
        eyebrow=u"Toujours disponible",
        titre=u"Votre panier n’a pas bougé",
        apercu=u"Si quelque chose vous a fait hésiter, dites-le-nous.",
        corps=u"".join([
            P.format(u"Bonjour,"),
            P.format(u"Votre panier vous attend toujours. Si quelque chose vous a fait hésiter "
                     u"sur le choix du soin, la formule ou le délai de livraison, "
                     u"dites-le-nous."),
            P.format(u"Chez Irizée, les formules sont courtes&nbsp;: un actif par besoin, et la "
                     u"raison pour laquelle il est là. Si vous hésitez entre deux soins, "
                     u"nous vous aidons à choisir."),
        ]),
        bouton=u"Reprendre ma commande",
        question=u"Répondez simplement à cet e-mail, nous lisons tout.",
    ),
    dict(
        f=u"panier-abandonne-3.html",
        eyebrow=u"Dernier rappel",
        titre=u"Dernier rappel",
        apercu=u"On vous le garde encore un peu.",
        corps=u"".join([
            P.format(u"Bonjour,"),
            P.format(u"C’est le dernier message que nous vous envoyons au sujet de ce panier."),
            P.format(u"Il reste accessible&nbsp;: si vous souhaitez le reprendre, c’est en un "
                     u"clic. Sinon, nous n’en reparlerons plus."),
        ]),
        bouton=u"Reprendre ma commande",
        question=u"Une question ? Répondez à cet e-mail, nous lisons tout.",
    ),
]

ici = os.path.dirname(os.path.abspath(__file__))

for e in EMAILS:
    html = GABARIT.format(
        bg=BG, ink=INK, surface=SURFACE, line=LINE, card=CARD,
        text2=TEXT2, muted=MUTED, font=FONT, logo=LOGO,
        eyebrow=e["eyebrow"], titre=e["titre"], apercu=e["apercu"],
        corps=e["corps"], bouton=e["bouton"], question=e["question"],
    )
    chemin = os.path.join(ici, e["f"])
    io.open(chemin, "w", encoding="utf-8").write(html)
    print(e["f"], len(html), "caracteres")

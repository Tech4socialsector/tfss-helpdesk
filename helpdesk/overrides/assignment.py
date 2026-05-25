import frappe
from frappe import _
from frappe.desk.doctype.notification_log.notification_log import (
    enqueue_create_notification,
    get_title,
)


def notify_assignment(
    assigned_by, allocated_to, doc_type, doc_name, action="CLOSE", description=None
):
    """
    Override of frappe.desk.form.assign_to.notify_assignment
    Sends branded email for HD Ticket assignments and unassignments.
    All other doctypes use the default plain Frappe behaviour.
    """
    if not (assigned_by and allocated_to and doc_type and doc_name):
        return

    assigned_user = frappe.db.get_value(
        "User", allocated_to, ["language", "enabled"], as_dict=True
    )

    # return if self-assigned or user disabled
    if assigned_by == allocated_to or not assigned_user.enabled:
        return

    user_name = frappe.get_cached_value("User", frappe.session.user, "full_name")
    title = get_title(doc_type, doc_name)

    if doc_type == "HD Ticket":

        if action == "CLOSE":
            # ── BRANDED UNASSIGNMENT EMAIL ──────────────────────────────
            subject = f"Ticket {doc_name} — Assignment Removed"
            description_html = f"""
<body style="margin:0; padding:30px 20px; background:transparent; font-family:Arial, sans-serif;">
  <table align="center" border="0" cellpadding="0" cellspacing="0"
    style="width:660px; max-width:660px; border:1px solid #e0e0e0; border-radius:10px; overflow:hidden; border-collapse:separate;">

    <!-- HEADER -->
    <tr>
      <td colspan="3" style="background-color:#00A6C8; padding:16px 24px; border-radius:10px 10px 0 0;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%">
          <tr>
            <td>
              <img src="/files/Logo APF.png" alt="Azim Premji Foundation" width="95"
                style="display:block; background:#fff; padding:5px 8px; border-radius:6px;" />
            </td>
            <td align="right" valign="middle">
              <p style="margin:0; font-size:12px; font-weight:700; color:#ffffff;">Support Help Desk</p>
              <p style="margin:2px 0 0; font-size:10px; color:rgba(255,255,255,0.75);">Tech for Social Sector &middot; Azim Premji Foundation</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>

    <!-- ORANGE LINE -->
    <tr>
      <td colspan="3" bgcolor="#FF6B1A" height="3"
        style="font-size:0; line-height:0; height:3px; background-color:#FF6B1A;">&nbsp;</td>
    </tr>

    <!-- TWO COLUMNS -->
    <tr>

      <!-- LEFT -->
      <td valign="top" bgcolor="#f7fbfd"
        style="width:190px; min-width:190px; max-width:190px; padding:22px 18px; background-color:#f7fbfd; vertical-align:top;">

        <table border="0" cellpadding="0" cellspacing="0" style="margin-bottom:14px;">
          <tr>
            <td align="center" valign="middle"
              style="width:36px; height:36px; background-color:#FF6B1A; border-radius:50%; text-align:center; vertical-align:middle;">
              <span style="font-size:18px; color:#ffffff; line-height:36px;">&#10005;</span>
            </td>
            <td style="padding-left:10px; font-size:12px; font-weight:700; color:#FF6B1A; vertical-align:middle;">
              Assignment Removed
            </td>
          </tr>
        </table>

        <table border="0" cellpadding="0" cellspacing="0" width="100%">
          <tr><td height="1" bgcolor="#dce8ee"
            style="font-size:0; line-height:0; height:1px; background-color:#dce8ee;">&nbsp;</td></tr>
        </table>

        <p style="margin:14px 0 3px; font-size:9px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:#FF6B1A;">Ticket ID</p>
        <p style="margin:0 0 14px; font-size:24px; font-weight:700; color:#00A6C8; line-height:1;">{doc_name}</p>

        <p style="margin:0 0 2px; font-size:9px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:#FF6B1A;">Removed By</p>
        <p style="margin:0 0 16px; font-size:12px; color:#333333; line-height:1.4;">{user_name}</p>

        <table border="0" cellpadding="0" cellspacing="0" width="100%">
          <tr><td height="1" bgcolor="#dce8ee"
            style="font-size:0; line-height:0; height:1px; background-color:#dce8ee;">&nbsp;</td></tr>
        </table>

        <p style="margin:14px 0 0; font-size:12px; font-weight:700; color:#222222;">Tech for Social Sector</p>
        <p style="margin:2px 0 0; font-size:10px; color:#00A6C8;">Azim Premji Foundation</p>
        <a href="mailto:tech4socialsector@azimpremjifoundation.org"
           style="display:block; margin-top:5px; font-size:10px; color:#00A6C8; text-decoration:underline; word-break:break-all;">
          tech4socialsector@azimpremjifoundation.org
        </a>

        <!-- BUTTON -->
        <table border="0" cellpadding="0" cellspacing="0" style="margin-top:16px;">
          <tr>
            <td bgcolor="#00A6C8" style="background-color:#00A6C8; border-radius:6px 0 0 6px;">
              <a href="/helpdesk/tickets/{doc_name}"
                style="display:inline-block; padding:10px 14px; font-size:12px; font-weight:700; color:#ffffff; text-decoration:none;">
                View Ticket
              </a>
            </td>
            <td bgcolor="#FF6B1A" style="background-color:#FF6B1A; border-radius:0 6px 6px 0;">
              <a href="/helpdesk/tickets/{doc_name}"
                style="display:inline-block; padding:10px 11px; font-size:14px; font-weight:700; color:#ffffff; text-decoration:none;">
                &#8594;
              </a>
            </td>
          </tr>
        </table>

      </td>

      <!-- DIVIDER -->
      <td bgcolor="#FF6B1A" width="3"
        style="width:3px; min-width:3px; background-color:#FF6B1A; font-size:0; line-height:0;">&nbsp;</td>

      <!-- RIGHT -->
      <td valign="top" style="padding:22px 22px 18px; vertical-align:top;">

        <p style="margin:0 0 3px; font-size:13px; color:#888888;">Hello,</p>
        <p style="margin:0 0 16px; font-size:16px; font-weight:700; color:#222222; line-height:1.3;">
          Your assignment has been removed.
        </p>
        <p style="margin:0 0 20px; font-size:13px; color:#555555; line-height:1.7;">
          Your assignment on the following ticket has been removed by <strong>{user_name}</strong>.
          No further action is required from your end unless reassigned.
        </p>

        <!-- DETAIL BLOCK -->
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom:20px;">
          <tr>
            <td width="4" bgcolor="#00A6C8"
              style="width:4px; background-color:#00A6C8; border-radius:3px 0 0 3px; font-size:0;">&nbsp;</td>
            <td width="3" bgcolor="#FF6B1A"
              style="width:3px; background-color:#FF6B1A; font-size:0;">&nbsp;</td>
            <td style="background-color:#f5fbfd; padding:14px 16px; border:1px solid #d0eaf4; border-left:none;">
              <table border="0" cellpadding="0" cellspacing="0" width="100%">
                <tr>
                  <td style="padding-bottom:10px;">
                    <p style="margin:0 0 2px; font-size:9px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:#7ab8c8;">Ticket</p>
                    <p style="margin:0; font-size:13px; font-weight:700; color:#222222;">{doc_name}</p>
                  </td>
                </tr>
                <tr>
                  <td style="border-top:1px solid #dce8ee; padding-top:10px; padding-bottom:10px;">
                    <p style="margin:0 0 2px; font-size:9px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:#7ab8c8;">Subject</p>
                    <p style="margin:0; font-size:13px; color:#333333;">{title}</p>
                  </td>
                </tr>
                <tr>
                  <td style="border-top:1px solid #dce8ee; padding-top:10px;">
                    <p style="margin:0 0 2px; font-size:9px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:#7ab8c8;">Removed By</p>
                    <p style="margin:0; font-size:13px; color:#333333;">{user_name}</p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>

        <p style="margin:0 0 2px; font-size:13px; color:#555555;">Regards,</p>
        <p style="margin:0; font-size:13px; font-weight:700; color:#222222;">Support Team</p>

      </td>
    </tr>

    <!-- ALERT BAR -->
    <tr>
      <td colspan="3" bgcolor="#fff8e6"
        style="background-color:#fff8e6; border-top:1px solid #ffe0a0; padding:10px 24px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%">
          <tr>
            <td width="22" valign="middle" style="padding-right:8px;">
              <div style="width:18px; height:18px; background-color:#FF6B1A; border-radius:50%;
                text-align:center; font-size:11px; font-weight:700; color:#ffffff; line-height:18px;">!</div>
            </td>
            <td style="font-size:11px; color:#996600; line-height:1.5; vertical-align:middle;">
              <strong>Automated email</strong> &mdash; Please do not reply to this email.
            </td>
          </tr>
        </table>
      </td>
    </tr>

    <!-- BASE STRIPE -->
    <tr>
      <td colspan="3" style="padding:0; font-size:0; line-height:0;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%">
          <tr>
            <td bgcolor="#00A6C8" height="5"
              style="background-color:#00A6C8; height:5px; width:66%; font-size:0;">&nbsp;</td>
            <td bgcolor="#FF6B1A" height="5"
              style="background-color:#FF6B1A; height:5px; width:34%; font-size:0;">&nbsp;</td>
          </tr>
        </table>
      </td>
    </tr>

  </table>
</body>"""

        else:
            # ── BRANDED ASSIGNMENT EMAIL ────────────────────────────────
            subject = f"New Ticket Assigned to You — {doc_name}"
            description_html = f"""
<body style="margin:0; padding:30px 20px; background:transparent; font-family:Arial, sans-serif;">
  <table align="center" border="0" cellpadding="0" cellspacing="0"
    style="width:660px; max-width:660px; border:1px solid #e0e0e0; border-radius:10px; overflow:hidden; border-collapse:separate;">

    <!-- HEADER -->
    <tr>
      <td colspan="3" style="background-color:#00A6C8; padding:16px 24px; border-radius:10px 10px 0 0;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%">
          <tr>
            <td>
              <img src="/files/Logo APF.png" alt="Azim Premji Foundation" width="95"
                style="display:block; background:#fff; padding:5px 8px; border-radius:6px;" />
            </td>
            <td align="right" valign="middle">
              <p style="margin:0; font-size:12px; font-weight:700; color:#ffffff;">Support Help Desk</p>
              <p style="margin:2px 0 0; font-size:10px; color:rgba(255,255,255,0.75);">Tech for Social Sector &middot; Azim Premji Foundation</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>

    <!-- ORANGE LINE -->
    <tr>
      <td colspan="3" bgcolor="#FF6B1A" height="3"
        style="font-size:0; line-height:0; height:3px; background-color:#FF6B1A;">&nbsp;</td>
    </tr>

    <!-- TWO COLUMNS -->
    <tr>

      <!-- LEFT -->
      <td valign="top" bgcolor="#f7fbfd"
        style="width:190px; min-width:190px; max-width:190px; padding:22px 18px; background-color:#f7fbfd; vertical-align:top;">

        <table border="0" cellpadding="0" cellspacing="0" style="margin-bottom:14px;">
          <tr>
            <td align="center" valign="middle"
              style="width:36px; height:36px; background-color:#00A6C8; border-radius:50%; text-align:center; vertical-align:middle;">
              <span style="font-size:18px; color:#ffffff; line-height:36px;">&#128100;</span>
            </td>
            <td style="padding-left:10px; font-size:12px; font-weight:700; color:#00A6C8; vertical-align:middle;">
              New Assignment
            </td>
          </tr>
        </table>

        <table border="0" cellpadding="0" cellspacing="0" width="100%">
          <tr><td height="1" bgcolor="#dce8ee"
            style="font-size:0; line-height:0; height:1px; background-color:#dce8ee;">&nbsp;</td></tr>
        </table>

        <p style="margin:14px 0 3px; font-size:9px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:#FF6B1A;">Ticket ID</p>
        <p style="margin:0 0 14px; font-size:24px; font-weight:700; color:#00A6C8; line-height:1;">{doc_name}</p>

        <p style="margin:0 0 2px; font-size:9px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:#FF6B1A;">Assigned By</p>
        <p style="margin:0 0 16px; font-size:12px; color:#333333; line-height:1.4;">{user_name}</p>

        <table border="0" cellpadding="0" cellspacing="0" width="100%">
          <tr><td height="1" bgcolor="#dce8ee"
            style="font-size:0; line-height:0; height:1px; background-color:#dce8ee;">&nbsp;</td></tr>
        </table>

        <p style="margin:14px 0 0; font-size:12px; font-weight:700; color:#222222;">Tech for Social Sector</p>
        <p style="margin:2px 0 0; font-size:10px; color:#00A6C8;">Azim Premji Foundation</p>
        <a href="mailto:tech4socialsector@azimpremjifoundation.org"
           style="display:block; margin-top:5px; font-size:10px; color:#00A6C8; text-decoration:underline; word-break:break-all;">
          tech4socialsector@azimpremjifoundation.org
        </a>

        <!-- BUTTON -->
        <table border="0" cellpadding="0" cellspacing="0" style="margin-top:16px;">
          <tr>
            <td bgcolor="#00A6C8" style="background-color:#00A6C8; border-radius:6px 0 0 6px;">
              <a href="/helpdesk/tickets/{doc_name}"
                style="display:inline-block; padding:10px 14px; font-size:12px; font-weight:700; color:#ffffff; text-decoration:none;">
                Open Ticket
              </a>
            </td>
            <td bgcolor="#FF6B1A" style="background-color:#FF6B1A; border-radius:0 6px 6px 0;">
              <a href="/helpdesk/tickets/{doc_name}"
                style="display:inline-block; padding:10px 11px; font-size:14px; font-weight:700; color:#ffffff; text-decoration:none;">
                &#8594;
              </a>
            </td>
          </tr>
        </table>

      </td>

      <!-- DIVIDER -->
      <td bgcolor="#FF6B1A" width="3"
        style="width:3px; min-width:3px; background-color:#FF6B1A; font-size:0; line-height:0;">&nbsp;</td>

      <!-- RIGHT -->
      <td valign="top" style="padding:22px 22px 18px; vertical-align:top;">

        <p style="margin:0 0 3px; font-size:13px; color:#888888;">Hello,</p>
        <p style="margin:0 0 16px; font-size:16px; font-weight:700; color:#222222; line-height:1.3;">
          A ticket has been assigned to you.
        </p>
        <p style="margin:0 0 20px; font-size:13px; color:#555555; line-height:1.7;">
          A new Helpdesk ticket has been assigned to you. Please review the details and take action at your earliest convenience.
        </p>

        <!-- DETAIL BLOCK -->
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom:20px;">
          <tr>
            <td width="4" bgcolor="#00A6C8"
              style="width:4px; background-color:#00A6C8; border-radius:3px 0 0 3px; font-size:0;">&nbsp;</td>
            <td width="3" bgcolor="#FF6B1A"
              style="width:3px; background-color:#FF6B1A; font-size:0;">&nbsp;</td>
            <td style="background-color:#f5fbfd; padding:14px 16px; border:1px solid #d0eaf4; border-left:none;">
              <table border="0" cellpadding="0" cellspacing="0" width="100%">
                <tr>
                  <td style="padding-bottom:10px;">
                    <p style="margin:0 0 2px; font-size:9px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:#7ab8c8;">Ticket</p>
                    <p style="margin:0; font-size:13px; font-weight:700; color:#222222;">{doc_name}</p>
                  </td>
                </tr>
                <tr>
                  <td style="border-top:1px solid #dce8ee; padding-top:10px; padding-bottom:10px;">
                    <p style="margin:0 0 2px; font-size:9px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:#7ab8c8;">Subject</p>
                    <p style="margin:0; font-size:13px; color:#333333;">{title}</p>
                  </td>
                </tr>
                <tr>
                  <td style="border-top:1px solid #dce8ee; padding-top:10px;">
                    <p style="margin:0 0 2px; font-size:9px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:#7ab8c8;">Assigned By</p>
                    <p style="margin:0; font-size:13px; color:#333333;">{user_name}</p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>

        <p style="margin:0 0 2px; font-size:13px; color:#555555;">Regards,</p>
        <p style="margin:0; font-size:13px; font-weight:700; color:#222222;">Support Team</p>

      </td>
    </tr>

    <!-- ALERT BAR -->
    <tr>
      <td colspan="3" bgcolor="#fff8e6"
        style="background-color:#fff8e6; border-top:1px solid #ffe0a0; padding:10px 24px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%">
          <tr>
            <td width="22" valign="middle" style="padding-right:8px;">
              <div style="width:18px; height:18px; background-color:#FF6B1A; border-radius:50%;
                text-align:center; font-size:11px; font-weight:700; color:#ffffff; line-height:18px;">!</div>
            </td>
            <td style="font-size:11px; color:#996600; line-height:1.5; vertical-align:middle;">
              <strong>Automated email</strong> &mdash; Please do not reply to this email.
              Open the ticket using the link above.
            </td>
          </tr>
        </table>
      </td>
    </tr>

    <!-- BASE STRIPE -->
    <tr>
      <td colspan="3" style="padding:0; font-size:0; line-height:0;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%">
          <tr>
            <td bgcolor="#00A6C8" height="5"
              style="background-color:#00A6C8; height:5px; width:66%; font-size:0;">&nbsp;</td>
            <td bgcolor="#FF6B1A" height="5"
              style="background-color:#FF6B1A; height:5px; width:34%; font-size:0;">&nbsp;</td>
          </tr>
        </table>
      </td>
    </tr>

  </table>
</body>"""

    else:
        # ── NON HD TICKET: keep default plain Frappe behaviour ──────────
        from frappe.desk.doctype.notification_log.notification_log import get_title_html

        if action == "CLOSE":
            subject = _(
                "Your assignment on {0} {1} has been removed by {2}",
                lang=assigned_user.language,
            ).format(
                frappe.bold(_(doc_type)),
                get_title_html(title),
                frappe.bold(user_name),
            )
        else:
            subject = _(
                "{0} assigned a new task {1} {2} to you",
                lang=assigned_user.language,
            ).format(
                frappe.bold(user_name),
                frappe.bold(_(doc_type, lang=assigned_user.language)),
                get_title_html(title),
            )
        description_html = f"<div>{description}</div>" if description else None

    notification_doc = {
        "type": "Assignment",
        "document_type": doc_type,
        "subject": subject,
        "document_name": doc_name,
        "from_user": frappe.session.user,
        "email_content": description_html,
    }

    enqueue_create_notification(allocated_to, notification_doc)
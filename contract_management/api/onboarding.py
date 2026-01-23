import frappe
from frappe import _
from frappe.utils import now_datetime, nowdate
import json

# ============================================
# DASHBOARD APIs
# ============================================

@frappe.whitelist(allow_guest=True)
def get_dashboard_stats():
    """Dashboard ke liye stats return karta hai"""
    try:
        # Employee Contracts se stats nikalo
        contracts = frappe.get_all(
            'Employee Contract',
            fields=['name', 'status', 'seasonal_work', 'creation']
        )
        
        stats = {
            'active': 0,
            'onboarding': 0,
            'pending': 0,
            'renewals': 0,
            'pool': 0,
            'terminated': 0,
            'total': len(contracts)
        }
        
        for contract in contracts:
            if contract.get('status') == 'Contract Signed':
                stats['active'] += 1
            elif contract.get('status') == 'Waiting for Contract':
                stats['onboarding'] += 1
            elif contract.get('status') == 'Waiting for Candidate':
                stats['pending'] += 1
            elif contract.get('status') == 'Renewal in Progress':
                stats['renewals'] += 1
            elif contract.get('status') == 'Rejected':
                stats['terminated'] += 1
            
            # Seasonal pool count
            if contract.get('seasonal_work') == 1 and contract.get('status') == 'Contract Signed':
                stats['pool'] += 1
        
        return {'success': True, 'data': stats}
    
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'Dashboard Stats Error')
        return {'success': False, 'message': str(e)}


@frappe.whitelist(allow_guest=True)
def get_all_contracts(filters=None):
    """All contracts with filtering"""
    try:
        filter_dict = {}
        
        if filters:
            if isinstance(filters, str):
                filters = json.loads(filters)
            
            # Status filter
            if filters.get('status'):
                filter_dict['status'] = filters['status']
            
            # Seasonal filter
            if filters.get('seasonal_only'):
                filter_dict['seasonal_work'] = 1
        
        contracts = frappe.get_all(
            'Employee Contract',
            fields=[
                'name', 'first_name', 'middle_name', 'last_name',
                'applicant_email', 'status', 'verification_id',
                'estimated_starting_date', 'estimated_finish_date',
                'creation', 'seasonal_work', 'probationary_employment',
                'probationary_employment_period_in_month'
            ],
            filters=filter_dict,
            order_by='creation desc'
        )
        
        return {'success': True, 'data': contracts}
    
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'Get Contracts Error')
        return {'success': False, 'message': str(e)}


# ============================================
# OPERATIONS APIs
# ============================================

@frappe.whitelist(allow_guest=True)
def get_pipeline_data():
    """Operations pipeline ke liye data"""
    try:
        # Step 1: Invitation - Waiting for Candidate
        invitations = frappe.get_all(
            'Job Offer',
            filters={'status': 'Awaiting Response'},
            fields=['name', 'applicant_name', 'applicant_email', 'offer_date']
        )
        
        # Step 2: Data Entry - In Progress (Job Applicant)
        data_entry = frappe.get_all(
            'Job Applicant',
            filters={'status': 'Open'},
            fields=['name', 'applicant_name', 'email_id', 'job_title']
        )
        
        # Step 3: Contract - Ready for Signature
        ready_contracts = frappe.get_all(
            'Employee Contract',
            filters={'status': 'Waiting for Contract'},
            fields=[
                'name', 'first_name', 'last_name', 'applicant_email',
                'verification_id', 'estimated_starting_date'
            ]
        )
        
        return {
            'success': True,
            'data': {
                'invitations': invitations,
                'data_entry': data_entry,
                'ready_for_contract': ready_contracts,
                'stats': {
                    'invitation_count': len(invitations),
                    'data_entry_count': len(data_entry),
                    'contract_count': len(ready_contracts)
                }
            }
        }
    
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'Pipeline Data Error')
        return {'success': False, 'message': str(e)}


# ============================================
# INVITATION / CANDIDATE APIs
# ============================================

@frappe.whitelist(allow_guest=True)
def invite_candidate(data):
    """Only creates a Prospect Applicant record"""
    try:
        if isinstance(data, str):
            data = json.loads(data)
        
        # Step 1: Prospect Applicant ONLY
        prospect = frappe.get_doc({
            'doctype': 'Prospect Applicant',
            'first_name': data.get('first_name'),
            'middle_name': data.get('middle_name', ''),
            'last_name': data.get('last_name'),
            'email': data.get('email'),
            'full_name': f"{data.get('first_name')} {data.get('middle_name', '')} {data.get('last_name')}".strip()
        })
        prospect.insert(ignore_permissions=True)
        
        # COMMIT the change to the database
        frappe.db.commit()
        
        return {
            'success': True,
            'message': 'Prospect Applicant created successfully',
            'data': {
                'prospect': prospect.name
            }
        }
    
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(frappe.get_traceback(), 'Invite Candidate Error')
        return {'success': False, 'message': str(e)}


# ============================================
# WIZARD / FORM APIs
# ============================================

@frappe.whitelist(allow_guest=True)
def get_wizard_data(token):
    """Wizard ke liye candidate ka data"""
    try:
        # Token se Job Offer nikalo
        job_offer = frappe.get_doc('Job Offer', token)
        
        # Job Applicant data
        job_applicant = frappe.get_doc('Job Applicant', job_offer.job_applicant)
        
        return {
            'success': True,
            'data': {
                'job_offer': job_offer.as_dict(),
                'job_applicant': job_applicant.as_dict()
            }
        }
    
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'Get Wizard Data Error')
        return {'success': False, 'message': 'Invalid or expired token'}


@frappe.whitelist(allow_guest=True)
def submit_wizard_data(token, data):
    """Wizard form submit hone par"""
    try:
        if isinstance(data, str):
            data = json.loads(data)
        
        # Job Offer validate karo
        job_offer = frappe.get_doc('Job Offer', token)
        
        # Employee Contract banao
        contract = frappe.get_doc({
            'doctype': 'Employee Contract',
            'verification_id': job_offer.name,
            'first_name': data.get('first_name'),
            'middle_name': data.get('middle_name', ''),
            'last_name': data.get('last_name'),
            'applicant_email': data.get('email'),
            'applicant_contact_number': data.get('phone'),
            'date_of_birth': data.get('dob'),
            'gender': data.get('gender'),
            'country_of_birth': data.get('country_of_birth'),
            'citizenship': data.get('citizenship'),
            
            # Address
            'applicant_address': data.get('address'),
            'city_emp': data.get('city'),
            'state__province': data.get('state'),
            'country_emp': data.get('country'),
            'zip__postal_code': data.get('zip'),
            
            # Bank
            'bank': data.get('bank'),
            'bic_code': data.get('bic'),
            'your_bank_account_number': data.get('account_number'),
            
            # Emergency Contact
            'emergency_contact_first_name': data.get('emergency_first_name'),
            'emergency_contact_last_name': data.get('emergency_last_name'),
            'emergency_contact_mobile_phone_number': data.get('emergency_phone'),
            
            # Status
            'status': 'Waiting for Contract',
            'creation_time': now_datetime()
        })
        
        contract.insert(ignore_permissions=True)
        
        # Job Offer status update
        job_offer.status = 'Accepted'
        job_offer.save(ignore_permissions=True)
        
        frappe.db.commit()
        
        # HR ko email bhejo
        send_hr_notification(contract)
        
        return {
            'success': True,
            'message': 'Application submitted successfully',
            'contract_id': contract.name
        }
    
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(frappe.get_traceback(), 'Submit Wizard Error')
        return {'success': False, 'message': str(e)}


def send_hr_notification(contract):
    """HR ko notify karo ki contract ready hai"""
    try:
        hr_emails = frappe.get_all(
            'Has Role',
            filters={'role': 'Hr Executive', 'parenttype': 'User'},
            fields=['parent']
        )
        
        recipients = [user.parent for user in hr_emails]
        
        if not recipients:
            recipients = [frappe.session.user]
        
        subject = f"New Contract Ready for Signature - {contract.first_name} {contract.last_name}"
        
        message = f"""
        <h3>Contract Ready for Review</h3>
        <p>A new employment contract is ready for your signature:</p>
        <ul>
            <li><strong>Candidate:</strong> {contract.first_name} {contract.last_name}</li>
            <li><strong>Email:</strong> {contract.applicant_email}</li>
            <li><strong>Contract ID:</strong> {contract.name}</li>
        </ul>
        <p><a href="{frappe.utils.get_url()}/app/employee-contract/{contract.name}">View Contract</a></p>
        """
        
        frappe.sendmail(
            recipients=recipients,
            subject=subject,
            message=message,
            now=True
        )
    
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'HR Notification Error')


# ============================================
# CONTRACT SIGNING APIs
# ============================================

@frappe.whitelist(allow_guest=True)
def sign_contract(contract_id, signature_data):
    """HR signature for contract"""
    try:
        contract = frappe.get_doc('Employee Contract', contract_id)
        
        # Signature save karo
        contract.signature_from_employer = signature_data
        contract.completion_sign_time = now_datetime()
        contract.status = 'Contract Signed'
        
        contract.save(ignore_permissions=True)
        frappe.db.commit()
        
        # Candidate ko email bhejo
        send_contract_signed_email(contract)
        
        return {
            'success': True,
            'message': 'Contract signed successfully'
        }
    
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(frappe.get_traceback(), 'Sign Contract Error')
        return {'success': False, 'message': str(e)}


def send_contract_signed_email(contract):
    """Candidate ko email bhejo ki contract signed ho gaya"""
    try:
        subject = "Your Employment Contract is Signed!"
        
        message = f"""
        <h3>Hello {contract.first_name},</h3>
        <p>Great news! Your employment contract has been signed and approved.</p>
        <p><strong>Contract ID:</strong> {contract.name}</p>
        <p><strong>Start Date:</strong> {contract.estimated_starting_date or 'TBD'}</p>
        <p>Welcome to the team!</p>
        <br>
        <p>Best regards,<br>HR Team</p>
        """
        
        frappe.sendmail(
            recipients=[contract.applicant_email],
            subject=subject,
            message=message,
            now=True
        )
    
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'Contract Signed Email Error')


# ============================================
# EMPLOYEE CREATION API - WITH ALL CUSTOM FIELDS
# ============================================

@frappe.whitelist(allow_guest=True)
def create_employee(data):
    """Employee DocType mein new entry banao with all custom fields"""
    try:
        if isinstance(data, str):
            data = json.loads(data)
        
        # Required fields validation
        if not data.get('first_name') or not data.get('last_name'):
            return {
                'success': False,
                'message': 'First Name and Last Name are required'
            }
        
        # Company handling
        company_name = data.get('company', '').strip()
        if not company_name:
            companies = frappe.get_all('Company', fields=['name'], limit=1)
            if companies:
                company_name = companies[0].name
            else:
                return {'success': False, 'message': 'No company found'}
        
        if not frappe.db.exists('Company', company_name):
            companies = frappe.get_all('Company', fields=['name'], limit=1)
            if companies:
                company_name = companies[0].name
        
        # Date conversions
        date_of_birth = None
        if data.get('birthday'):
            try:
                from datetime import datetime
                try:
                    dob = datetime.strptime(data.get('birthday'), '%d-%m-%Y')
                    date_of_birth = dob.strftime('%Y-%m-%d')
                except:
                    try:
                        dob = datetime.strptime(data.get('birthday'), '%Y-%m-%d')
                        date_of_birth = dob.strftime('%Y-%m-%d')
                    except:
                        pass
            except:
                pass
        
        # Date of joining
        from frappe.utils import nowdate
        date_of_joining = data.get('date_of_joining') or nowdate()
        
        # Employee data with ALL custom fields
        employee_data = {
            'doctype': 'Employee',
            
            # Basic Required Fields
            'naming_series': 'HR-EMP-',
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'company': company_name,
            'date_of_joining': date_of_joining,
            'status': 'Active',
            
            # Optional Standard Fields
            'middle_name': data.get('middle_name', ''),
            'gender': data.get('gender', ''),
            'date_of_birth': date_of_birth,
            
            # Custom Fields - Personal Info
            'custom_employeeid': data.get('employment_id', ''),
            'custom_preferred_name': data.get('preferred_name', ''),
            'custom_entity_id': data.get('entity_id', ''),
            'custom_work_place_id': data.get('work_place_id', ''),
            'custom_country_of_birth': data.get('country_of_birth', ''),
            'custom_citizenship': data.get('citizenship', ''),
            
            # Custom Fields - Contact & Employment
            'custom_contact_number': data.get('mobile_phone', ''),
            'custom_email_address': data.get('email', ''),
            'custom_end_date': data.get('end_date', ''),
            
            # Standard Contact Fields
            'cell_number': data.get('mobile_phone', ''),
            'personal_email': data.get('email', ''),
            'employee_number': data.get('employment_id', ''),
        }
        
        # Create employee
        employee = frappe.get_doc(employee_data)
        employee.insert(ignore_permissions=True)
        
        frappe.db.commit()
        
        return {
            'success': True,
            'message': 'Employee created successfully!',
            'employee_id': employee.name,
            'employee_number': employee.employee_number or employee.custom_employeeid,
            'company': company_name
        }
    
    except Exception as e:
        frappe.db.rollback()
        error_msg = str(e)
        frappe.log_error(frappe.get_traceback(), 'Create Employee Error')
        return {'success': False, 'message': error_msg}


# ============================================
# UTILITY APIs
# ============================================

@frappe.whitelist(allow_guest=True)
def delete_contract(contract_id):
    """Contract delete karo"""
    try:
        frappe.delete_doc('Employee Contract', contract_id, ignore_permissions=True)
        frappe.db.commit()
        
        return {'success': True, 'message': 'Contract deleted'}
    
    except Exception as e:
        frappe.db.rollback()
        return {'success': False, 'message': str(e)}


@frappe.whitelist(allow_guest=True)
def resend_invitation(job_offer_id):
    """Invitation email phir se bhejo"""
    try:
        job_offer = frappe.get_doc('Job Offer', job_offer_id)
        
        wizard_link = f"{frappe.utils.get_url()}/onboarding/wizard?token={job_offer.name}"
        subject = f"Job Offer - {job_offer.designation}"
        message = f"""
        <h3>Hello {job_offer.applicant_name},</h3>
        <p>Congratulations! We are pleased to offer you the position of <strong>{job_offer.designation}</strong>.</p>
        <p>Please complete your application by clicking the link below:</p>
        <p><a href="{wizard_link}">Complete Your Application</a></p>
        """
        
        frappe.sendmail(
            recipients=[job_offer.applicant_email],
            subject=subject,
            message=message,
            now=True
        )
        
        return {'success': True, 'message': 'Invitation resent'}
    
    except Exception as e:
        return {'success': False, 'message': str(e)}
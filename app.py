import os
from pathlib import Path
from datetime import datetime

from flask import Flask, jsonify, redirect, request, send_from_directory, session, url_for
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

database_url = os.getenv("DATABASE_URL", "").strip()
if database_url.startswith("postgres://"):
	database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)
elif database_url.startswith("postgresql://"):
	database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

if not database_url:
	database_url = f"sqlite:///{(BASE_DIR / 'database.db').as_posix()}"

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
db = SQLAlchemy(app)


def current_time() -> datetime:
	return datetime.now().astimezone()


class User(db.Model):
	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100), nullable=False, unique=True, index=True)
	password_hash = db.Column(db.String(255), nullable=False)


class Volunteer(db.Model):
	__tablename__ = "volunteers"

	id = db.Column(db.Integer, primary_key=True)
	volunteer_code = db.Column(db.String(100), nullable=False, unique=True, index=True)
	password_hash = db.Column(db.String(255), nullable=False)
	created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=current_time)


class VolunteerProfile(db.Model):
	__tablename__ = "volunteer_profiles"

	id = db.Column(db.Integer, primary_key=True)
	volunteer_id = db.Column(db.Integer, db.ForeignKey("volunteers.id"), nullable=False, unique=True, index=True)
	gender = db.Column(db.String(30), nullable=False, default="Not specified")
	age_group = db.Column(db.String(30), nullable=False, default="Not specified")
	area = db.Column(db.String(120), nullable=False, default="Not specified")
	updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=current_time, onupdate=current_time)


class UserProfile(db.Model):
	__tablename__ = "user_profiles"

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True, index=True)
	name = db.Column(db.String(120), nullable=False, default="")
	phone = db.Column(db.String(40), nullable=False, default="")
	email = db.Column(db.String(120), nullable=False, default="")
	address = db.Column(db.String(255), nullable=False, default="")
	avatar_data = db.Column(db.Text, nullable=True)
	updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=current_time, onupdate=current_time)


class UserPreference(db.Model):
	__tablename__ = "user_preferences"

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True, index=True)
	app_language = db.Column(db.String(16), nullable=False, default="en")
	updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=current_time, onupdate=current_time)


class Report(db.Model):
	__tablename__ = "reports"

	id = db.Column(db.Integer, primary_key=True)
	case_id = db.Column(db.String(24), nullable=False, unique=True, index=True)
	condition = db.Column(db.String(50), nullable=False)
	address = db.Column(db.String(255), nullable=False)
	latitude = db.Column(db.String(32), nullable=True)
	longitude = db.Column(db.String(32), nullable=True)
	photo_data = db.Column(db.Text, nullable=True)
	status = db.Column(db.String(20), nullable=False, default="open")
	created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=current_time)


class ReportReporter(db.Model):
	__tablename__ = "report_reporters"

	id = db.Column(db.Integer, primary_key=True)
	report_id = db.Column(db.Integer, db.ForeignKey("reports.id"), nullable=False, unique=True, index=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)


class VolunteerCaseAssignment(db.Model):
	__tablename__ = "volunteer_case_assignments"

	id = db.Column(db.Integer, primary_key=True)
	report_id = db.Column(db.Integer, db.ForeignKey("reports.id"), nullable=False, unique=True, index=True)
	volunteer_id = db.Column(db.Integer, db.ForeignKey("volunteers.id"), nullable=False, index=True)
	assigned_at = db.Column(db.DateTime(timezone=True), nullable=False, default=current_time)
	resolved_at = db.Column(db.DateTime(timezone=True), nullable=True)


def serialize_report(report: Report) -> dict:
	reporter_name = "Reporter"
	reporter_phone = "Phone unavailable"
	reporter_avatar_data = None
	reporter_link = ReportReporter.query.filter_by(report_id=report.id).first()

	if reporter_link is not None:
		reporter_user = User.query.get(reporter_link.user_id)
		if reporter_user is not None:
			reporter_profile = UserProfile.query.filter_by(user_id=reporter_user.id).first()
			reporter_name = (reporter_profile.name if reporter_profile and reporter_profile.name else reporter_user.username) or "Reporter"
			reporter_phone = (reporter_profile.phone if reporter_profile and reporter_profile.phone else "Phone unavailable")
			reporter_avatar_data = reporter_profile.avatar_data if reporter_profile and reporter_profile.avatar_data else None

	return {
		"id": report.case_id,
		"condition": report.condition,
		"address": report.address,
		"latitude": report.latitude,
		"longitude": report.longitude,
		"photoData": report.photo_data,
		"status": report.status,
		"reporterName": reporter_name,
		"reporterPhone": reporter_phone,
		"reporterAvatarData": reporter_avatar_data,
		"submittedAt": report.created_at.isoformat() if report.created_at else current_time().isoformat(),
	}


with app.app_context():
	db.create_all()


def is_authenticated() -> bool:
	return bool(session.get("user_id"))


def is_volunteer_authenticated() -> bool:
	return bool(session.get("volunteer_id"))


def unauthorized_json_response():
	return jsonify({"error": "Unauthorized"}), 401


def get_or_create_user_profile(user: User) -> UserProfile:
	profile = UserProfile.query.filter_by(user_id=user.id).first()
	if profile is None:
		profile = UserProfile(
			user_id=user.id,
			name=user.username,
		)
		db.session.add(profile)
		db.session.commit()
	return profile


def get_or_create_volunteer_profile(volunteer: Volunteer) -> VolunteerProfile:
	profile = VolunteerProfile.query.filter_by(volunteer_id=volunteer.id).first()
	if profile is None:
		profile = VolunteerProfile(volunteer_id=volunteer.id)
		db.session.add(profile)
		db.session.commit()
	return profile


def get_or_create_user_preference(user: User) -> UserPreference:
	preference = UserPreference.query.filter_by(user_id=user.id).first()
	if preference is None:
		preference = UserPreference(user_id=user.id)
		db.session.add(preference)
		db.session.commit()
	return preference


def get_or_assign_latest_open_report_for_volunteer(volunteer: Volunteer):
	assigned_open_report = (
		db.session.query(Report)
		.join(VolunteerCaseAssignment, VolunteerCaseAssignment.report_id == Report.id)
		.filter(
			VolunteerCaseAssignment.volunteer_id == volunteer.id,
			Report.status == "open",
		)
		.order_by(Report.created_at.desc())
		.first()
	)

	if assigned_open_report:
		return assigned_open_report

	unassigned_open_report = (
		db.session.query(Report)
		.outerjoin(VolunteerCaseAssignment, VolunteerCaseAssignment.report_id == Report.id)
		.filter(
			Report.status == "open",
			VolunteerCaseAssignment.id.is_(None),
		)
		.order_by(Report.created_at.desc())
		.first()
	)

	if unassigned_open_report:
		assignment = VolunteerCaseAssignment(
			report_id=unassigned_open_report.id,
			volunteer_id=volunteer.id,
		)
		db.session.add(assignment)
		db.session.commit()

	return unassigned_open_report


@app.get("/")
def root():
	if is_volunteer_authenticated():
		return redirect(url_for("pages", filename="volunteer_dashboard.html"))
	if is_authenticated():
		return redirect(url_for("index_page"))
	return redirect(url_for("login_page"))


@app.route("/login", methods=["GET", "POST"])
def login_page():
	if request.method == "POST":
		username = (request.form.get("username") or "").strip()
		password = (request.form.get("password") or "").strip()

		if not username or not password:
			return redirect(url_for("login_page"))

		user = User.query.filter_by(username=username).first()

		if user is None:
			user = User(
				username=username,
				password_hash=generate_password_hash(password),
			)
			db.session.add(user)
			db.session.commit()
		elif not check_password_hash(user.password_hash, password):
			return redirect(url_for("login_page"))

		get_or_create_user_profile(user)
		session["user_id"] = user.id
		session["username"] = user.username
		return redirect(url_for("index_page"))

	return send_from_directory(BASE_DIR, "login.html")


@app.get("/index")
def index_page():
	if not is_authenticated():
		return redirect(url_for("login_page"))
	return send_from_directory(BASE_DIR, "index.html")


@app.route("/volunteer-auth", methods=["GET", "POST"])
def volunteer_auth_page():
	if request.method == "POST":
		action = (request.form.get("action") or "login").strip().lower()
		volunteer_code = (request.form.get("volunteer_id") or "").strip()
		password = (request.form.get("password") or "").strip()

		if not volunteer_code or not password:
			return redirect(url_for("volunteer_auth_page"))

		volunteer = Volunteer.query.filter(func.lower(Volunteer.volunteer_code) == volunteer_code.lower()).first()

		if action == "register":
			if volunteer is None:
				volunteer = Volunteer(
					volunteer_code=volunteer_code,
					password_hash=generate_password_hash(password),
				)
				db.session.add(volunteer)
				db.session.commit()
				get_or_create_volunteer_profile(volunteer)
			elif not check_password_hash(volunteer.password_hash, password):
				return redirect(url_for("volunteer_auth_page"))
		elif action == "login":
			if volunteer is None or not check_password_hash(volunteer.password_hash, password):
				return redirect(url_for("volunteer_auth_page"))
		else:
			return redirect(url_for("volunteer_auth_page"))

		session["volunteer_id"] = volunteer.id
		session["volunteer_code"] = volunteer.volunteer_code
		return redirect(url_for("pages", filename="volunteer_dashboard.html"))

	if is_volunteer_authenticated():
		return redirect(url_for("pages", filename="volunteer_dashboard.html"))

	return send_from_directory(BASE_DIR, "volunteer_auth.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
	session.clear()
	return redirect(url_for("login_page"))


@app.route("/volunteer-logout", methods=["GET", "POST"])
def volunteer_logout():
	session.pop("volunteer_id", None)
	session.pop("volunteer_code", None)
	return redirect(url_for("index_page"))


@app.get("/api/profile")
def get_profile():
	if not is_authenticated():
		return unauthorized_json_response()

	user = User.query.get(session.get("user_id"))
	if user is None:
		return unauthorized_json_response()

	profile = get_or_create_user_profile(user)
	preference = get_or_create_user_preference(user)

	return jsonify(
		{
			"profile": {
				"name": profile.name or user.username,
				"phone": profile.phone or "",
				"email": profile.email or "",
				"address": profile.address or "",
				"avatarData": profile.avatar_data,
				"appLanguage": preference.app_language or "en",
			}
		}
	), 200


@app.put("/api/profile")
def update_profile():
	if not is_authenticated():
		return unauthorized_json_response()

	user = User.query.get(session.get("user_id"))
	if user is None:
		return unauthorized_json_response()

	payload = request.get_json(silent=True) or {}
	name = str(payload.get("name") or "").strip()
	phone = str(payload.get("phone") or "").strip()
	email = str(payload.get("email") or "").strip()
	address = str(payload.get("address") or "").strip()
	avatar_data = payload.get("avatarData")
	app_language = str(payload.get("appLanguage") or "").strip().lower()
	allowed_languages = {"en", "hi", "bn", "ta", "te", "mr", "gu"}

	if not name:
		return jsonify({"error": "Name is required"}), 400
	if not phone:
		return jsonify({"error": "Phone is required"}), 400
	if app_language and app_language not in allowed_languages:
		return jsonify({"error": "Invalid app language"}), 400

	profile = get_or_create_user_profile(user)
	preference = get_or_create_user_preference(user)
	profile.name = name
	profile.phone = phone
	profile.email = email
	profile.address = address
	if avatar_data is not None:
		profile.avatar_data = str(avatar_data) if avatar_data else None
	if app_language:
		preference.app_language = app_language

	db.session.commit()

	return jsonify(
		{
			"profile": {
				"name": profile.name,
				"phone": profile.phone,
				"email": profile.email,
				"address": profile.address,
				"avatarData": profile.avatar_data,
				"appLanguage": preference.app_language or "en",
			}
		}
	), 200


@app.put("/api/profile/language")
def update_profile_language():
	if not is_authenticated():
		return unauthorized_json_response()

	user = User.query.get(session.get("user_id"))
	if user is None:
		return unauthorized_json_response()

	payload = request.get_json(silent=True) or {}
	app_language = str(payload.get("appLanguage") or "").strip().lower()
	allowed_languages = {"en", "hi", "bn", "ta", "te", "mr", "gu"}

	if app_language not in allowed_languages:
		return jsonify({"error": "Invalid app language"}), 400

	preference = get_or_create_user_preference(user)
	preference.app_language = app_language
	db.session.commit()

	return jsonify({"appLanguage": preference.app_language}), 200


@app.get("/api/profile/stats")
def profile_stats():
	if not is_authenticated():
		return unauthorized_json_response()

	total_reports = Report.query.count()
	resolved_reports = Report.query.filter_by(status="resolved").count()
	open_reports = Report.query.filter_by(status="open").count()

	return jsonify(
		{
			"stats": {
				"totalReports": total_reports,
				"resolvedReports": resolved_reports,
				"openReports": open_reports,
				"community": 0,
				"badges": 0,
			}
		}
	), 200


@app.post("/api/reports")
def create_report():
	if not is_authenticated():
		return unauthorized_json_response()

	user = User.query.get(session.get("user_id"))
	if user is None:
		return unauthorized_json_response()

	payload = request.get_json(silent=True) or {}
	condition = str(payload.get("condition") or "").strip()
	address = str(payload.get("address") or "").strip()
	latitude = str(payload.get("latitude") or "").strip()
	longitude = str(payload.get("longitude") or "").strip()
	photo_data = payload.get("photoData")

	if not condition:
		condition = "Injured"

	if not address:
		return jsonify({"error": "Address is required"}), 400

	if not photo_data:
		return jsonify({"error": "Photo is required"}), 400

	case_id = "R" + str(int(current_time().timestamp() * 1000))[-6:]
	while Report.query.filter_by(case_id=case_id).first() is not None:
		case_id = "R" + str(int(current_time().timestamp() * 1000) + 1)[-6:]

	report = Report(
		case_id=case_id,
		condition=condition,
		address=address,
		latitude=latitude or None,
		longitude=longitude or None,
		photo_data=str(photo_data),
		status="open",
	)
	db.session.add(report)
	db.session.commit()

	reporter_link = ReportReporter(report_id=report.id, user_id=user.id)
	db.session.add(reporter_link)
	db.session.commit()

	return jsonify({"report": serialize_report(report)}), 201


@app.get("/api/reports/latest")
def latest_report():
	if not (is_authenticated() or is_volunteer_authenticated()):
		return unauthorized_json_response()

	latest = Report.query.filter_by(status="open").order_by(Report.created_at.desc()).first()

	if latest is None:
		return jsonify({"report": None}), 200

	return jsonify({"report": serialize_report(latest)}), 200


@app.get("/api/reports/open")
def open_reports():
	if not (is_authenticated() or is_volunteer_authenticated()):
		return unauthorized_json_response()

	reports = (
		Report.query.filter_by(status="open")
		.order_by(Report.created_at.desc())
		.limit(100)
		.all()
	)

	return jsonify({"reports": [serialize_report(report) for report in reports]}), 200


@app.get("/api/reports/<case_id>")
def report_by_case_id(case_id: str):
	if not (is_authenticated() or is_volunteer_authenticated()):
		return unauthorized_json_response()

	report = Report.query.filter_by(case_id=case_id).first()
	if report is None:
		return jsonify({"error": "Report not found"}), 404

	return jsonify({"report": serialize_report(report)}), 200


@app.get("/api/reports/sections")
def report_sections():
	if not is_authenticated():
		return unauthorized_json_response()

	current_reports = (
		Report.query.filter_by(status="open")
		.order_by(Report.created_at.desc())
		.limit(50)
		.all()
	)
	past_reports = (
		Report.query.filter_by(status="resolved")
		.order_by(Report.created_at.desc())
		.limit(50)
		.all()
	)

	return jsonify(
		{
			"current": [serialize_report(report) for report in current_reports],
			"past": [serialize_report(report) for report in past_reports],
		}
	), 200


@app.patch("/api/reports/<case_id>/resolve")
def resolve_report(case_id: str):
	if not is_volunteer_authenticated():
		return unauthorized_json_response()

	current_volunteer = Volunteer.query.get(session.get("volunteer_id"))
	if current_volunteer is None:
		return unauthorized_json_response()

	report = Report.query.filter_by(case_id=case_id).first()
	if report is None:
		return jsonify({"error": "Report not found"}), 404

	assignment = VolunteerCaseAssignment.query.filter_by(report_id=report.id).first()
	if assignment is None:
		assignment = VolunteerCaseAssignment(
			report_id=report.id,
			volunteer_id=current_volunteer.id,
		)
		db.session.add(assignment)
	else:
		assignment.volunteer_id = current_volunteer.id

	if report.status == "resolved":
		return jsonify({"report": serialize_report(report), "message": "Already resolved"}), 200

	report.status = "resolved"
	assignment.resolved_at = current_time()
	db.session.commit()

	return jsonify({"report": serialize_report(report), "message": "Case marked as resolved"}), 200


@app.get("/api/dashboard/volunteer-summary")
def volunteer_summary():
	if not is_volunteer_authenticated():
		return unauthorized_json_response()

	current_volunteer = Volunteer.query.get(session.get("volunteer_id"))
	if current_volunteer is None:
		return unauthorized_json_response()

	total_reports = VolunteerCaseAssignment.query.filter_by(volunteer_id=current_volunteer.id).count()
	resolved_reports = (
		VolunteerCaseAssignment.query.filter(
			VolunteerCaseAssignment.volunteer_id == current_volunteer.id,
			VolunteerCaseAssignment.resolved_at.isnot(None),
		).count()
	)
	open_reports = Report.query.filter_by(status="open").count()
	latest = Report.query.filter_by(status="open").order_by(Report.created_at.desc()).first()

	latest_report_data = serialize_report(latest) if latest else None
	volunteer_code = current_volunteer.volunteer_code if current_volunteer else ""
	volunteer_profile = get_or_create_volunteer_profile(current_volunteer) if current_volunteer else None

	return jsonify(
		{
			"summary": {
				"totalReports": total_reports,
				"resolvedReports": resolved_reports,
				"openReports": open_reports,
				"currentVolunteerCode": volunteer_code,
				"currentVolunteerDemographics": {
					"gender": volunteer_profile.gender if volunteer_profile else "Not specified",
					"ageGroup": volunteer_profile.age_group if volunteer_profile else "Not specified",
					"area": volunteer_profile.area if volunteer_profile else "Not specified",
					"memberSince": current_volunteer.created_at.strftime("%d %b %Y") if current_volunteer and current_volunteer.created_at else "Not available",
				},
				"latestReport": latest_report_data,
			}
		}
	), 200


@app.get("/api/volunteer/profile")
def get_volunteer_profile():
	if not is_volunteer_authenticated():
		return unauthorized_json_response()

	current_volunteer = Volunteer.query.get(session.get("volunteer_id"))
	if current_volunteer is None:
		return unauthorized_json_response()

	profile = get_or_create_volunteer_profile(current_volunteer)

	return jsonify(
		{
			"profile": {
				"volunteerCode": current_volunteer.volunteer_code,
				"gender": profile.gender or "Not specified",
				"ageGroup": profile.age_group or "Not specified",
				"area": profile.area or "Not specified",
				"memberSince": current_volunteer.created_at.strftime("%d %b %Y") if current_volunteer.created_at else "Not available",
			}
		}
	), 200


@app.put("/api/volunteer/profile")
def update_volunteer_profile():
	if not is_volunteer_authenticated():
		return unauthorized_json_response()

	current_volunteer = Volunteer.query.get(session.get("volunteer_id"))
	if current_volunteer is None:
		return unauthorized_json_response()

	payload = request.get_json(silent=True) or {}
	gender = str(payload.get("gender") or "").strip() or "Not specified"
	age_group = str(payload.get("ageGroup") or "").strip() or "Not specified"
	area = str(payload.get("area") or "").strip() or "Not specified"

	profile = get_or_create_volunteer_profile(current_volunteer)
	profile.gender = gender
	profile.age_group = age_group
	profile.area = area
	db.session.commit()

	return jsonify(
		{
			"profile": {
				"volunteerCode": current_volunteer.volunteer_code,
				"gender": profile.gender,
				"ageGroup": profile.age_group,
				"area": profile.area,
				"memberSince": current_volunteer.created_at.strftime("%d %b %Y") if current_volunteer.created_at else "Not available",
			}
		}
	), 200


@app.get("/api/time/current")
def current_server_time():
	now = current_time()
	return jsonify(
		{
			"currentTime": now.isoformat(),
			"timezone": str(now.tzinfo),
			"unix": int(now.timestamp()),
		}
	), 200


@app.get("/assets/<path:filename>")
def assets(filename: str):
	return send_from_directory(ASSETS_DIR, filename)


@app.get("/<path:filename>")
def pages(filename: str):
	allowed_files = {
		"index.html",
		"login.html",
		"volunteer_auth.html",
		"login.css",
		"login-bg.jpg",
		"profile.html",
		"profile_edit.html",
		"report.html",
		"track_updates.html",
		"vDashboard1.html",
		"volunteer_dashboard.html",
	}
	protected_files = {
		"index.html",
		"profile.html",
		"profile_edit.html",
		"report.html",
		"track_updates.html",
	}
	volunteer_only_files = {
		"volunteer_dashboard.html",
		"vDashboard1.html",
	}

	if filename in allowed_files:
		if filename in protected_files and not is_authenticated():
			return redirect(url_for("login_page"))
		if filename in volunteer_only_files and not is_volunteer_authenticated():
			return redirect(url_for("volunteer_auth_page"))
		return send_from_directory(BASE_DIR, filename)

	return ("Not Found", 404)


if __name__ == "__main__":
	app.run(debug=True)

"""Interactive command-line interface."""
from app.core.config import ensure_data_files
from app.core.exceptions import StudentSystemError
from app.models.enums import CourseLevel
from app.repositories.course_repository import CourseRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.course_service import CourseService
from app.services.student_service import StudentService
from app.utils.helpers import format_record

class Application: # noqa: D101
    """Coordinate repositories, services, and the CLI menus."""
    def __init__(self) -> None:
        ensure_data_files()
        self.auth = AuthService(UserRepository())
        self.students = StudentService(StudentRepository(), CourseRepository(), self.auth)
        self.courses = CourseService(CourseRepository(), self.auth)

    def run(self) -> None:
        """Run the application until the user chooses exit."""
        while True:
            if not self.auth.is_authenticated:
                if not self._guest_menu():
                    break
            else:
                self._main_menu()

    def _guest_menu(self) -> bool:
        print("\n" + "=" * 45)
        print("       STUDENT MINI SYSTEM")
        print("=" * 45)
        print("1. Register")
        print("2. Login")
        print("0. Exit")
        choice = input("Choose: ").strip()
        try:
            if choice == "1":
                self._register()
            elif choice == "2":
                self._login()
            elif choice == "0":
                return False
            else:
                print("Invalid choice.")
        except (StudentSystemError, ValueError) as exc:
            print(f"Error: {exc}")
        return True

    def _register(self) -> None:
        user = self.auth.register(input("Username: "), input("Password: "))
        print(f"Registered successfully: {user.username}")

    def _login(self) -> None:
        user = self.auth.login(input("Username: "), input("Password: "))
        print(f"Welcome, {user.username}!")

    def _main_menu(self) -> None:
        print("\n" + "=" * 45)
        print("             MAIN MENU")
        print("=" * 45)
        print("1. Add Student")
        print("2. View Students")
        print("3. Add Course")
        print("4. View Courses")
        print("5. Enroll Student")
        print("6. Add / Update Grade")
        print("7. Calculate Student Average")
        print("8. Show Top Students")
        print("9. Logout")
        print("0. Exit")
        choice = input("Choose: ").strip()
        try:
            actions = {
                "1": self._add_student, "2": self._view_students, "3": self._add_course,
                "4": self._view_courses, "5": self._enroll, "6": self._grade,
                "7": self._average, "8": self._top_students,
            }
            if choice in actions:
                actions[choice]()
            elif choice == "9":
                self.auth.logout()
                print("Logged out.")
            elif choice == "0":
                raise SystemExit
            else:
                print("Invalid choice.")
        except (StudentSystemError, ValueError) as exc:
            print(f"Error: {exc}")

    def _add_student(self) -> None:
        student = self.students.add_student(input("Name: "), int(input("Age: ")), major=input("Major: "))
        print(f"Created: {student}")

    def _view_students(self) -> None:
        students = self.students.get_all_students()
        if not students:
            print("No students found.")
        for student in students:
            print(format_record("Student", student.student_id, student.name, major=student.major))

    def _add_course(self) -> None:
        name = input("Course name: ")
        hours = int(input("Hours: "))
        date = input("Start date (YYYY-MM-DD): ")
        course = self.courses.add_course(name, hours, date, level=CourseLevel.BEGINNER)
        print(f"Created: {course}")

    def _view_courses(self) -> None:
        courses = self.courses.get_all_courses()
        if not courses:
            print("No courses found.")
        for course in courses:
            print(f"{course.course_id} | {course.course_name} | {course.hours} hours | {course.level.value}")

    def _enroll(self) -> None:
        self.students.enroll_student(input("Student ID: "), input("Course ID: "))
        print("Enrollment completed.")

    def _grade(self) -> None:
        self.students.set_grade(input("Student ID: "), input("Course ID: "), float(input("Grade (0-100): ")))
        print("Grade saved.")

    def _average(self) -> None:
        average = self.students.calculate_average(input("Student ID: "))
        print(f"Average: {average:.2f}")

    def _top_students(self) -> None:
        for index, student in enumerate(self.students.get_top_students(), 1):
            print(f"{index}. {student.name} - {student.average():.2f}")

def run_cli() -> None:
    """Create and run the CLI application."""
    Application().run()

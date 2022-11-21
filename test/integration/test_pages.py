"""
Integration tests for Flask app
"""
from app import app


def test_healthcheck():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/health' route is requested (GET)
    THEN "Ok" should be sent back to signify healthy server
    """

    with app.test_client() as test_client:
        response = test_client.get('/health')

        assert response.status_code == 200
        assert b"Ok" == response.data


def test_home_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """

    with app.test_client() as test_client:
        response = test_client.get('/')

        assert response.status_code == 200
        assert b"Upload an Excel file" in response.data


def test_upload_route():
    """
    GIVEN a Flask application configured for testing
    WHEN /upload (POST) is hit with a file in the body
    THEN the file should be searched in 'processed.lst'
    """

    # clear processed.lst contents
    with open('processed.lst', 'w', encoding="utf-8"):
        pass

    with app.test_client() as test_client:
        filename = 'examples/expedia_report_monthly_january_2018.xlsx'

        with open(filename, 'rb') as file:
            data = {
                "file": (file, filename)
            }

            response = test_client.post('/upload', data=data)

            # it should send ok the first time
            assert response.status_code == 200

        with open(filename, 'rb') as file:
            data = {
                "file": (file, filename)
            }

            response = test_client.post('/upload', data=data)

            # it should fail the second time
            # and push a flash message to the Flask session
            assert response.status_code == 302

            with test_client.session_transaction() as session:
                flash = session['_flashes'][0]

                assert flash[0] == 'message'
                assert flash[1].endswith('has already been processed')


def test_upload_invalid_files():
    """
    GIVEN a Flask application configured for testing
    WHEN /upload (POST) is hit with a malformed file in the body
    THEN the file should be flagged as such and the function should exit
    """

    # clear processed.lst contents
    with open('processed.lst', 'w', encoding="utf-8"):
        pass

    with app.test_client() as test_client:
        filename = 'examples/expedia_report_monthly_q1.xlsx'

        with open(filename, 'rb') as file:
            data = {
                "file": (file, filename)
            }

            response = test_client.post('/upload', data=data)

            # it should send ok the first time
            assert response.status_code == 302

            with test_client.session_transaction() as session:
                flash = session['_flashes'][0]

                assert flash[0] == 'message'
                assert flash[1] == "Error: malformed speadsheet"

        filename = 'examples/expedia_report_monthly_march_march.xlsx'

        with open(filename, 'rb') as file:
            data = {
                "file": (file, filename)
            }

            response = test_client.post('/upload', data=data)

        filename = 'examples/unreal_percent_janubad_2018.xlsx'

        with open(filename, 'rb') as file:
            data = {
                "file": (file, filename)
            }

            response = test_client.post('/upload', data=data)

            assert response.status_code == 302

            with test_client.session_transaction() as session:
                flash = session['_flashes'][-1]

                assert flash[0] == 'message'
                assert flash[1].startswith('Some of the data in')
                assert flash[1].endswith('is invalid!')

        filename = 'examples/missing_sheets_janubad_2018.xlsx'

        with open(filename, 'rb') as file:
            data = {
                "file": (file, filename)
            }

            response = test_client.post('/upload', data=data)

            assert response.status_code == 302

            with test_client.session_transaction() as session:
                flash = session['_flashes'][-1]

                assert flash[0] == 'message'
                assert flash[1] == "Error: malformed speadsheet"


def test_no_file_uploaded():
    """
    GIVEN a Flask application configured for testing
    WHEN submit is clicked without selecting a file first
    THEN check the flash warning was rendered
    """

    with app.test_client() as test_client:
        response = test_client.post('/upload', data={
            "file": (b'', '')
        })

        assert b'Redirecting...' in response.data

        with test_client.session_transaction() as session:
            flash = session['_flashes'][0]

            assert flash[0] == 'message'
            assert flash[1] == 'No file uploaded'


def test_404_page():
    """
    GIVEN a Flask application configured for testing
    WHEN an unknown route is requested
    THEN the user should be taken to the 404 page
    """

    with app.test_client() as test_client:
        response = test_client.get('/fhauief')

        assert b'Page not found' in response.data

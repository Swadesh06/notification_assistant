import unittest
from unittest.mock import patch, MagicMock
from email_reader import connect_to_email

class TestEmailReader(unittest.TestCase):
    @patch('imaplib.IMAP4_SSL')
    def test_connect_to_email(self, mock_imap):
        mock_mail = MagicMock()
        mock_imap.return_value = mock_mail

        result = connect_to_email()

        mock_imap.assert_called_once_with('imap.gmail.com', 993)
        mock_mail.login.assert_called_once_with('your-email@gmail.com', 'your-password')
        mock_mail.select.assert_called_once_with('inbox')
        self.assertEqual(result, mock_mail)

if __name__ == '__main__':
    unittest.main()
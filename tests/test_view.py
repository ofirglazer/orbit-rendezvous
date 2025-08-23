import pytest
from unittest.mock import Mock, patch, MagicMock
from src.orbit_view import OrbitRenderer
from src.orbit_model import GameModel


class TestOrbitView:

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.image.load')
    def test_view_initialization(self, mock_image_load, mock_display, mock_init):

        # Setup mock return values
        mock_screen = Mock()  # Fake screen object
        mock_display.return_value = mock_screen  # set_mode returns fake screen
        mock_image_load.return_value = MagicMock()  # Fake surface object

        # mock_font_instance = Mock()  # Fake font object
        # mock_font.return_value = mock_font_instance  # Font() returns fake font

        # Create view - this will call mocked functions
        view = OrbitRenderer(800, 600)

        # Verify pygame.init was called
        mock_init.assert_called_once()
        print("✓ pygame.init() was called")

        # Verify display.set_mode was called with correct parameters
        mock_display.assert_called_once_with((800, 600))
        print("✓ pygame.display.set_mode((800, 600)) was called")

        # Verify image.load was called with correct parameters
        mock_image_load.assert_called_once_with("stars-galaxy.jpg")
        print('✓ pygame.image.load(\"stars-galaxy.jpg\") was called')

        # # Verify font creation was called
        # assert mock_font.call_count >= 1  # Should be called at least once
        # print("✓ pygame.font.Font() was called")

        # Verify view has expected attributes
        assert view.width == 800
        assert view.height == 600
        assert view.window == mock_screen  # Should reference our fake screen
        print("✓ All assertions passed!")

    '''def test_without_mocking_fails(self):
        """This test shows what happens WITHOUT mocking."""
        try:
            # This will try to actually initialize pygame!
            view = Orbit_renderer(800, 600)
            # If this runs in headless environment, it might fail
            print("Somehow pygame initialized successfully")
        except Exception as e:
            print(f"Failed without mocking: {e}")
            # This is expected in testing environments'''

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.image.load')
    @patch('pygame.draw.circle')
    @patch('pygame.display.flip')
    def test_render_calls_draw_method(self, mock_flip, mock_circle, mock_image_load, mock_display, mock_init):

        # Setup mock return values
        mock_screen = Mock()  # Fake screen object
        mock_display.return_value = mock_screen  # set_mode returns fake screen
        mock_image_load.return_value = MagicMock()  # Fake surface object

        # Create view - this will call mocked functions
        view = OrbitRenderer(400, 400)
        model = GameModel()
        view.render(model)

        # Should draw circles for ships
        assert mock_circle.call_count == len(model.ships) + 1  # one ship, one satellite, one star
        mock_flip.assert_called_once()

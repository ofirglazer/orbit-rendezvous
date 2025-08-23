import pygame
import pytest
from unittest.mock import patch, Mock, MagicMock
from src.orbit_controller import OrbitController


class TestGameController:

    @pytest.fixture
    def mock_pygame(self):
        """Mock pygame to avoid display requirements"""
        with patch('pygame.time.Clock'), \
                patch('pygame.image.load'), \
                patch('src.orbit_controller.GameModel') as MockModel, \
                patch('src.orbit_controller.OrbitRenderer') as MockView:
            yield MockModel, MockView

    @pytest.fixture
    def controller_with_mocks(self, mock_pygame):
        """Create controller with mocked dependencies"""
        MockModel, MockView = mock_pygame
        controller = OrbitController()
        controller.mock_model = MockModel.return_value
        controller.mock_view = MockView.return_value

        return controller

    # =============================================
    # 1. INITIALIZATION TESTING
    # =============================================

    def test_controller_initialization(self, mock_pygame):
        """Test controller initializes with correct default values"""
        controller = OrbitController()

        assert hasattr(controller, 'model')
        assert hasattr(controller, 'view')
        assert controller.running is True
        assert controller.paused is False
        assert controller.fps == 2

    def test_controller_custom_dimensions(self, mock_pygame):
        """Test controller accepts custom screen dimensions"""
        screen_width = 321
        screen_height = 123
        controller = OrbitController(screen_width, screen_height)
        MockModel, MockView = mock_pygame

        MockView.assert_called_with(screen_width, screen_height)

    # =============================================
    # 2. EVENT HANDLING TESTING
    # =============================================

    @patch('pygame.event.get')
    def test_quit_event_handling(self, mock_get_events, controller_with_mocks):
        """Test QUIT event sets running to False"""
        quit_event = MagicMock()
        quit_event.type = pygame.QUIT
        mock_get_events.return_value = [quit_event]

        initial_running = controller_with_mocks.running
        controller_with_mocks.handle_events()
        assert controller_with_mocks.running != initial_running

    @patch('pygame.event.get')
    def test_escape_key_handling(self, mock_get_events, controller_with_mocks):
        """Test ESC key sets running to False"""
        escape_event = MagicMock()
        escape_event.type = pygame.KEYDOWN
        escape_event.key = pygame.K_ESCAPE
        mock_get_events.return_value = [escape_event]

        initial_running = controller_with_mocks.running
        controller_with_mocks.handle_events()
        assert controller_with_mocks.running != initial_running

    @patch('pygame.event.get')
    def test_space_key_toggles_pause(self, mock_get_events, controller_with_mocks):
        """Test SPACE key toggles pause state"""
        space_event = MagicMock()
        space_event.type = pygame.KEYDOWN
        space_event.key = pygame.K_SPACE
        mock_get_events.return_value = [space_event]

        # Test pause toggle
        initial_pause = controller_with_mocks.paused
        controller_with_mocks.handle_events()
        assert controller_with_mocks.paused != initial_pause

        # Test toggle back
        controller_with_mocks.handle_events()
        assert controller_with_mocks.paused == initial_pause

    @patch('pygame.event.get')
    def test_up_arrows_increases_orbit(self, mock_get_events, controller_with_mocks):
        """Test UP arrow calls change_orbit(True)"""
        up_event = MagicMock()
        up_event.type = pygame.KEYDOWN
        up_event.key = pygame.K_UP
        mock_get_events.return_value = [up_event]

        controller_with_mocks.handle_events()
        controller_with_mocks.mock_model.change_orbit.assert_called_once_with(True)

    @patch('pygame.event.get')
    def test_down_arrows_decreases_orbit(self, mock_get_events, controller_with_mocks):
        """Test DOWN arrow calls change_orbit(False)"""
        up_event = MagicMock()
        up_event.type = pygame.KEYDOWN
        up_event.key = pygame.K_DOWN
        mock_get_events.return_value = [up_event]

        controller_with_mocks.handle_events()
        controller_with_mocks.mock_model.change_orbit.assert_called_once_with(False)

    @patch('pygame.event.get')
    def test_multiple_events_handling(self, mock_get_events, controller_with_mocks):
        """Test handling multiple events in one frame"""
        up_event = MagicMock()
        up_event.type = pygame.KEYDOWN
        up_event.key = pygame.K_UP
        space_event = MagicMock()
        space_event.type = pygame.KEYDOWN
        space_event.key = pygame.K_SPACE
        initial_pause = controller_with_mocks.paused

        # Both events should be processed
        mock_get_events.return_value = [space_event, up_event]
        controller_with_mocks.handle_events()
        assert controller_with_mocks.paused != initial_pause
        controller_with_mocks.mock_model.change_orbit.assert_called_once_with(True)

    @patch('pygame.event.get')
    def test_unknown_key_ignored(self, mock_get_events, controller_with_mocks):
        """Test that unknown keys are ignored gracefully"""
        unknown_event = MagicMock()
        unknown_event.type = pygame.KEYDOWN
        unknown_event.key = pygame.K_a  # not handled
        mock_get_events.return_value = [unknown_event]

        try:
            controller_with_mocks.handle_events()
        except Exception as e:
            pytest.fail(f"Unknown key should be ignored: {e}")

    # =============================================
    # 3. CLEANUP TESTING
    # =============================================

    @patch('pygame.quit')
    @patch('builtins.print')
    def test_cleanup(self, mock_print, mock_pygame_quit, controller_with_mocks):
        """Test cleanup calls pygame.quit and prints message"""
        controller_with_mocks.cleanup()

        mock_pygame_quit.assert_called_once()
        mock_print.assert_called_once_with("Game ended")

    # =============================================
    # 4. INTEGRATION TESTING
    # =============================================

    @patch('pygame.event.get')
    def test_model_view_coordination(self, mock_get_events, controller_with_mocks):
        """Test that controller properly coordinates model and view"""
        mock_get_events.return_value = []

        # Simulate game loop actions
        controller_with_mocks.mock_model.update()
        controller_with_mocks.mock_view.render(controller_with_mocks.mock_model)

        # Verify coordination
        controller_with_mocks.mock_model.update.assert_called()
        controller_with_mocks.mock_view.render.assert_called_with(controller_with_mocks.mock_model)

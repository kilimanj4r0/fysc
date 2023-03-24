import DetectorForm from './components/DetectorForm';
import CenteredPage from './components/Page/CenteredPage';

const renderPage = () => {
  return (
    <CenteredPage>
      <DetectorForm />
    </CenteredPage>
  );
};
const App = () => {
  return renderPage();
};

export default App;

import { css } from '@emotion/react';
import styled from '@emotion/styled';
import { Button, Card, Divider, Form, Input, Space, Typography, message } from 'antd';
import { useState } from 'react';

const { Title, Text } = Typography;

const CardWrapper = styled(Card)`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  max-width: var(--size-page-max-width);
`;

const CardHead = styled.div`
  text-align: center;
  padding: 1rem;
`;

const CardBodyStyle = {
  width: '100%',
};

const DetectorForm: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [loadingText, setLoadingText] = useState('Detect');
  const [resultShow, setResultShow] = useState(false);

  const onFinish = () => {
    message.success('Detection in progress!');
    // loading timeout
    setLoading(true);
    setLoadingText('Detecting');
    setTimeout(() => {
      setLoading(false);
      setResultShow(true);
      setLoadingText('Detected');
    }, 3000);
  };

  const onFinishFailed = () => {
    message.error('Detection failed!');
    setResultShow(false);
  };

  const onFill = () => {
    form.setFieldsValue({
      face: 'FACE',
      photos: 'PHOTOS',
    });
  };

  return (
    <CardWrapper
      title={
        <CardHead>
          <Title>fysc</Title>
          <Text>Provide links to Cloud (Yandex.Disk) directories</Text>
        </CardHead>
      }
      bodyStyle={CardBodyStyle}
    >
      <Form
        form={form}
        layout="vertical"
        onFinish={onFinish}
        onFinishFailed={onFinishFailed}
        autoComplete="off"
        requiredMark={false}
      >
        <Form.Item name="face" label="Face" rules={[{ type: 'url' }]}>
          <Input placeholder="cloud directory url" />
        </Form.Item>
        <Form.Item name="photos" label="Photos" rules={[{ type: 'url' }]}>
          <Input placeholder="cloud directory url" />
        </Form.Item>
        <Form.Item>
          <Space>
            <Button type="primary" htmlType="submit" loading={loading}>
              {loadingText}
            </Button>
            <Button htmlType="button" onClick={onFill} type="text">
              Fill form
            </Button>
          </Space>
        </Form.Item>
      </Form>
      {resultShow && <Text>Result</Text>}
    </CardWrapper>
  );
};

export default DetectorForm;

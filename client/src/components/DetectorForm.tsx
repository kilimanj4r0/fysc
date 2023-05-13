import styled from '@emotion/styled';
import { Button, Card, Form, Input, Space, Tooltip, Typography, message } from 'antd';
import { Rule } from 'antd/es/form';
import Link from 'antd/es/typography/Link';
import axios from 'axios';
import { useRef, useState } from 'react';

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
  const [loading, setLoading] = useState<boolean>(false);
  const [loadingText, setLoadingText] = useState<string>('Detect');
  const [filename, setFilename] = useState<string>('photos.zip');
  const [href, setHref] = useState<string>('');
  const ref = useRef<HTMLAnchorElement>(null);

  const onFinish = () => {
    setLoading(true);
    setLoadingText('Detecting');
    axios({
      url: 'http://localhost:8000/detector/find',
      method: 'GET',
      responseType: 'blob',
      params: {
        input_album_url: form.getFieldValue('input'),
        reference_album_url: form.getFieldValue('reference'),
      },
      headers: {
        Accept: 'application/octet-stream',
      },
      onDownloadProgress: (value) => {
        if (value.total) {
          setLoadingText(`Dowloading ${Math.round((value.loaded / value.total) * 100)}%`);
        } else if (value.download) {
          setLoadingText('Downloading');
        }
      },
    })
      .then((response) => {
        setFilename(response.headers['content-disposition'].split('filename=')[1].replace(/"/g, ''));
        setHref(URL.createObjectURL(response.data));
        setTimeout(() => ref.current?.click(), 100);
        setLoading(false);
        setLoadingText('Detect');
      })
      .catch((error) => {
        message.error('Detection failed!');
        setLoading(false);
        setLoadingText('Detect');
      });
  };

  const onFill = () => {
    form.setFieldsValue({
      reference: 'https://disk.yandex.com/d/ZOsKjMSGj6My2A',
      input: 'https://disk.yandex.ru/d/4WrRHSdG4gHf_w',
    });
  };

  const onClear = () => {
    form.resetFields();
  };

  const rules: Rule[] = [{ type: 'url' }, { required: true, message: 'Please input a valid url' }];

  return (
    <CardWrapper
      title={
        <CardHead>
          <Title>fysc</Title>
          <Text>Find your photos in shared albums</Text>
        </CardHead>
      }
      bodyStyle={CardBodyStyle}
    >
      <Form form={form} layout="vertical" onFinish={onFinish} autoComplete="off" requiredMark={true}>
        <Form.Item name="reference" label="Photos with your face" rules={rules}>
          <Input placeholder="cloud url" />
        </Form.Item>
        <Form.Item name="input" label="Photos to search" rules={rules}>
          <Input placeholder="cloud url" />
        </Form.Item>
        <Form.Item>
          <Space style={{ width: '100%' }} direction='vertical'>
            <Button type="primary" htmlType="submit" loading={loading} block>
              {loadingText}
            </Button>
            <Space>
              <Button htmlType="button" onClick={onFill}>
                Fill form
              </Button>
              <Button htmlType="button" onClick={onClear} type="text">
                Clear
              </Button>
            </Space>
          </Space>
        </Form.Item>
      </Form>
      <Link href={href} target="_blank" download={filename} ref={ref} style={{ display: 'none' }}>
        Download {filename}
      </Link>
      <Text type="secondary">Only Yandex.Disk is supported</Text>
    </CardWrapper>
  );
};

export default DetectorForm;

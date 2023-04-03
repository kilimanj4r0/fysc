import styled from '@emotion/styled';
import { Col, Layout, Row } from 'antd';
import React from 'react';
import { FCChildrenProps } from '../../types/common.types';

type Props = FCChildrenProps & JSX.IntrinsicElements['div'];

const CenteredLayout = styled(Layout)`
  height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-background);
`;

const CenteredPage: React.FC<Props> = ({ children }): JSX.Element => {
  return (
    <CenteredLayout>
      {children}
    </CenteredLayout>
  );
};

export default CenteredPage;
